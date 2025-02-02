import logging
from copy import deepcopy
from datetime import datetime
from typing import List

from django.db import transaction

from websecmap.organizations.models import Coordinate, Organization, OrganizationType, Url

log = logging.getLogger(__package__)

# implies that name + country + organization_type is unique.


@transaction.atomic
def merge(
    source_organizations_names: List[str],
    target_organization_name: str,
    when: datetime,
    organization_type: str = "municipality",
    country: str = "NL",
):
    """
    Keeping historical data correct is important.
    - The old organization should be visible, exactly as it was at that moment (geography), with the same ratings and
    urls.

    There are several strategies to merge:

    Situation 1: a new organization is created from older ones. This is recognizable due to a new name.
    - It copies all related data to itself. The history is needed to get a starting point / current rating.
    - A "created_on" is needed, so the new organization is not displayed in the past.
    - A "deleted_on" is needed on the previous organizations (with date + reason) so they are not shown in the future.

    Situation 2: an existing organization gets all the goodies:
    Solution 1: use the existing organization record:
    You cannot copy the history of the urls, as that changes the existing organization. It Can have the urls but they
    need to be re-scanned. This sounds like an aweful approach that mixes data. You might copy the last scans on the
    urls to get a starting point. But still: what is the advantage of mixing organizations like this? What if you want
    to undo this, then it's not clear what has been merged when. Just to save "one record" it adds a lot of complexity
    and opens the door to mistakes. We have to make solution 2 anyway, which is much clearer.

    Solution 2:
    The best way is to make a new organization and do the same as in situation 1.

    Optimizations:
    We have to take into account when rating an organization that it might be dead at some point. Also scans don't need
    to be performed after an organization is dead.

    In both scenario 1 and 2, a simple coordinate-copy is performed. This will employ the same pattern as other delete
    days: a created_on, a deleted_on (+date and reason). This way any coordinate layout can be valid for any
    organization.

    We can decide to only copy the last scan for each url, to get a starting history (we don't need anything before the
    merge, as that is already in other organizations). This way the organization starts out with the exact same data
    as the previous ones left off, without the (long) history.


    - Just alter the coordinates (and merge the old coordinates into one in this method, whereby you can import new
    coordinates from OSM, together with a date from when they are valid).

    Situation 3: special cases:
    Some villages are moved to another municipality. This means the urls have to be moved. This is currently not
    supported automatically and can be done by hand. It might be needed to make it easier to "transfer" an url
    to another organization "since" a certain date (effectively making also a copy, so the history of this URL stays
    in tact in the original old organization).


    Decisions:
    - Always make a new organization, weather it exists or not. (there are organizations with the same name, following
    the stacking pattern).
    - Make sure all coordinates from previous organization are assigned to the new one. They might be updated doing a
      coordinate import (some borders might move after at the final decision, even if it's miniscule).
    - The organization is added to all urls of all previous organizations, as it's now responsible for them.
    - We don't want duplicate urls in our system: this causes insane complexity.
    - Organizations are now displayed as:
    - Apeldoorn (Jan 2018) (current organization)
    - † Apeldoorn (Feb 2017) (dead organization)

    :param organizations:
    :param target_organization:
    :param when:
    :return:
    """

    type = OrganizationType.objects.get(name=organization_type)
    new_organization = Organization()
    new_organization.type = type
    new_organization.country = country
    new_organization.name = target_organization_name
    new_organization.created_on = when
    new_organization.is_dead = False

    # todo: ? Store information that the organization stems from a previous organization.

    # Get the currently existing organization
    # implies that name + country + organization_type is unique.
    try:
        original_target = Organization.objects.get(
            name=target_organization_name, country=country, type=type, is_dead=False
        )
        new_organization.twitter_handle = original_target.twitter_handle

        log.info("Creating a new %s, with information from the merged organization." % target_organization_name)
        original_target.is_dead = True
        original_target.is_dead_since = when
        original_target.is_dead_reason = (
            "Merged with other organizations, reusing the same name but different data" "+ the old data."
        )
        original_target.save()

        # save the clone of the organization. Because autherwise the above "get" will get two.
        new_organization.save()

        # copy all urls of the old organization to the new one. The new one has to be saved due to many to many rules.
        urls = Url.objects.all().filter(organization=original_target)
        for url in urls:
            url.organization.add(new_organization)
            url.save()

        # don't take the promises, they are from another organization and management

    except Organization.DoesNotExist:
        # well, it's not problem the old organization didnt exist. We're creating a new one.
        pass

    new_organization.save()

    for source_organizations_name in source_organizations_names:
        log.info("Trying to add %s to the merge with %s." % (source_organizations_name, new_organization))

        try:
            source_organization = Organization.objects.get(
                name=source_organizations_name, country=country, type=type, is_dead=False
            )
        except Organization.DoesNotExist:
            # New organizations don't exist... so nothing to migrate.
            raise ValueError(
                "Organization %s does not exist. Tried to merge it with %s. Are you using a different translation for "
                "this organization (for example a local dialect)?",
                source_organizations_name,
                target_organization_name,
            )

        # copy todays used coordinates from all to-be-merged organizations into the target
        for coordinate in Coordinate.objects.all().filter(organization=source_organization, is_dead=False):
            cloned_coordinate = deepcopy(coordinate)
            cloned_coordinate.id = None
            cloned_coordinate.created_on = when
            cloned_coordinate.organization = new_organization
            cloned_coordinate.save()
            # should the original coordinate die now? As it has been superseeded.
            # Would otherwise retrieve multiple coordinates.
            coordinate.is_dead = True
            coordinate.is_dead_since = when
            coordinate.is_dead_reason = "Merged with %s" % new_organization

        # Should we make copies of all urls? And for what? Or should we state somewhere when an URL was owned
        # by an organization? Like n-n with extra information from when that is valid? That would result in
        # even more administration overhead?

        # No: this should not answer "since when did what organization gain what access to an url".
        # This question might arise in the future, but it has never been an issue.
        # It is more then enough to have a date from when a (new) organization started to exist. This implies
        # that from that moment the URLS for that organization where valid.
        # This approach might result in a bit of overhead for rebuilds, but hey: it's less complicated with
        # less administration.

        # In any case, there should not be a duplicate of the Url: it only exists once (or stacking).

        # add the target to all urls managed by the source_organization
        # A weird bug in Django Jet doesn't show the urls in the new organization.
        # WRONG: you where looking at the old relation, not the many to many field(!).
        for url in Url.objects.all().filter(organization=source_organization):
            log.debug("Adding new organization to existing Url %s" % url)
            url.organization.add(new_organization)
            log.debug(url.organization.all())
            url.save()

        source_organization.is_dead = True
        source_organization.is_dead_since = when
        source_organization.is_dead_reason = "Merged into %s on %s." % (new_organization, when)
        source_organization.save()

    # raise NotImplemented
    # todo:
    # Update the map viewers, to only show the existing organizations at that time.


@transaction.atomic
def dissolve(
    dissolved_organization_name: str,
    target_organization_names: List[str],
    when: datetime,
    organization_type: str = "municipality",
    country: str = "NL",
):
    """
    Dissolving organizations leave behind a set of urls. Those urls should be taken care off by other existing
    organizations. This is not always the case unfortunately (but who will solve these issues otherwise?)

    :param source_organization_name:
    :param target_organization_names:
    :param when:
    :param organization_type:
    :param country:
    :return:
    """

    log.info("Dissolving %s into %s.", dissolved_organization_name, target_organization_names)

    type = OrganizationType.objects.get(name=organization_type)
    dissolved_organization = Organization.objects.get(
        name=dissolved_organization_name, country=country, type=type, is_dead=False
    )
    dissolved_organization.is_dead = True
    dissolved_organization.is_dead_since = when
    dissolved_organization.is_dead_reason = "Disolved into other organizations (%s)" % target_organization_names
    dissolved_organization.save()

    # the urls of this organization are shared to it's targets :) ENJOY! :)
    # but... "since when"? We don't store the date since when an url is relevant for an organization (yet) due to
    # administrative overhead. So we have to create a new organization with the merged urls. Otherwise
    # the history of the organization is poisoned. It seems we need this date field... :(

    for target_organization_name in target_organization_names:
        target_organization = Organization.objects.get(
            name=target_organization_name, country=country, type=type, is_dead=False
        )

        clone_target = deepcopy(target_organization)

        target_organization.is_dead = True
        target_organization.is_dead_since = when
        target_organization.is_dead_reason = (
            "Received heritage of dissolved organization %s" % dissolved_organization_name
        )
        target_organization.save()

        clone_target.id = None
        clone_target.created_on = when
        clone_target.save()

        # copy the urls to the clone.
        for url in Url.objects.all().filter(organization=target_organization):
            url.organization.add(clone_target)
            url.save()

        # enjoy solving the stuff of the other organizations...
        # they also get the dead urls, supposed they get back to life for some weird reason...
        # this includes cooperation urls and whatnot... good luck! This might result ins ome issues.
        urls = Url.objects.all().filter(organization=dissolved_organization)
        for url in urls:
            url.organization.add(clone_target)
            url.save()

        # don't take the promises, they are from another organization and management

    return


def add_url_to_new_organization(country: str, organization_type: str, target_organization_name, url, when):
    type = OrganizationType.objects.get(name=organization_type)

    organization = Organization.objects.get(name=target_organization_name, country=country, type=type, is_dead=False)

    new_url = Url()
    new_url.url = url
    new_url.created_on = when
    new_url.internal_notes = "Automatically created when new municipality was founded."
    new_url.save()

    new_url.organization.add(organization)
    new_url.save()
