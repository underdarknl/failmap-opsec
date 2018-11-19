import json
import logging
import os.path
import re
import subprocess
import time
import zipfile
from datetime import datetime
from subprocess import CalledProcessError
from typing import Dict, List
from urllib.error import HTTPError

import pytz
import requests
import tldextract
from clint.textui import progress
from constance import config
from django.conf import settings
from iso3166 import countries
from rdp import rdp
from wikidata.client import Client

from failmap.celery import app

from ..organizations.models import Coordinate, Organization, OrganizationType, Url
from .models import AdministrativeRegion

log = logging.getLogger(__package__)


"""
Todo: Possibility to remove water:
https://stackoverflow.com/questions/25297811/how-can-i-remove-water-from-openstreetmap-ways
https://gis.stackexchange.com/questions/157842/how-to-get-landmass-polygons-for-bounding-box-in-overpass-api/157943
https://stackoverflow.com/questions/41723087/get-administrative-borders-with-overpass-ql
"""


def get_resampling_resolution(country: str = "NL", organization_type: str = "municipality"):
    resolution = AdministrativeRegion.objects.all().filter(
        country=country,
        organization_type__name=organization_type).values_list('resampling_resolution', flat=True).first()

    if not resolution:
        return 0.001

    return resolution


def get_region(country: str = "NL", organization_type: str = "municipality"):
    return AdministrativeRegion.objects.all().filter(
        country=country,
        organization_type__name=organization_type).values_list('admin_level', flat=True).first()


# making this atomic makes sure that the database is locked in sqlite.
# The transaction is very very very very very very very very very very long
# You also cannot see progress...
# better to validate that the region doesn't exist and then add it...
# @transaction.atomic
@app.task(queue="storage")
def import_from_scratch(countries: List[str] = None, organization_types: List[str] = None, when=None):
    """
    Run this when you have nothing on the organization type in that country. It will help bootstrapping a
    certain region.

    :param countries: uppercase list of 2-letter country codes.
    :param organization_types: the types you want to import.
    :param when:
    :return:
    """

    log.info("Countries: %s" % countries)
    log.info("Region(s): %s" % organization_types)

    if not countries or countries == [None]:
        countries = ["NL"]

    # paramter hate causes organization_types == [None]
    if not organization_types or organization_types == [None]:
        log.info("Going to get all existing organization types, and try to import them all.")
        organization_types = list(OrganizationType.objects.all().values_list('name', flat=True))

    for country in countries:
        for organization_type in organization_types:

            if not get_region(country, organization_type):
                log.info("The combination of %s and %s does not exist in OSM. Skipping." % (country, organization_type))
                continue

            data = get_osm_data_wambachers(country, organization_type)
            for feature in data["features"]:

                if "properties" not in feature:
                    continue

                if "name" not in feature["properties"]:
                    continue

                resolution = get_resampling_resolution(country, organization_type)
                resampled = resample(feature, resolution)
                store_new(resampled, country, organization_type, when)

                # can't do multiprocessing.pool, given non global functions.

    log.info("Import finished.")


# @transaction.atomic
@app.task(queue="storage")
def update_coordinates(country: str = "NL", organization_type: str = "municipality", when=None):

    if not osmtogeojson_available():
        raise FileNotFoundError("osmtogeojson was not found. Please install it and make sure python can access it. "
                                "Cannot continue.")

    log.info("Attempting to update coordinates for: %s %s " % (country, organization_type))

    # you are about to load 50 megabyte of data. Or MORE! :)
    data = get_osm_data_wambachers(country, organization_type)

    log.info("Received coordinate data. Starting with: %s" % json.dumps(data)[0:200])

    log.info("Parsing features:")
    for feature in data["features"]:

        if "properties" not in feature:
            log.debug("Feature misses 'properties' property :)")
            continue

        if "name" not in feature["properties"]:
            log.debug("This feature does not contain a name: it might be metadata or something else.")
            continue

        # slower, but in a task. Still atomic this way.
        resolution = get_resampling_resolution(country, organization_type)
        store_updates(resample(feature, resolution), country, organization_type, when)

    log.info("Resampling and update tasks have been created.")


def resample(feature: Dict, resampling_resolution: float = 0.001):
    # downsample the coordinates using the rdp algorithm, mainly to reduce 50 megabyte to a about 150 kilobytes.
    # The code is a little bit dirty, using these counters. If you can refactor, please do :)

    log.info("Resampling path for %s" % feature["properties"]["name"])

    if feature["geometry"]["type"] == "Polygon":
        log.debug("Original length: %s" % len(feature["geometry"]["coordinates"][0]))
        i = 0
        for coordinate in feature["geometry"]["coordinates"]:
            feature["geometry"]["coordinates"][i] = rdp(coordinate, epsilon=resampling_resolution)
            i += 1
        log.debug("Resampled length: %s" % len(feature["geometry"]["coordinates"][0]))

    if feature["geometry"]["type"] == "MultiPolygon":
        i, j = 0, 0
        for coordinate in feature["geometry"]["coordinates"]:
            for nested_coordinate in feature["geometry"]["coordinates"][i]:
                feature["geometry"]["coordinates"][i][j] = rdp(nested_coordinate, epsilon=resampling_resolution)
                j += 1

            j = 0
            i += 1

    return feature


def store_new(feature: Dict, country: str = "NL", organization_type: str = "municipality", when=None):
    properties = feature["properties"]
    coordinates = feature["geometry"]

    """
    Handles the storing / administration of coordinates in failmap using the stacking pattern.

    "properties": {
                "@id": "relation/47394",
                "admin_level": "8",
                "authoritative": "yes",
                "boundary": "administrative",
                "name": "Heemstede",
                "ref:gemeentecode": "397",
                "source": "dataportal",
                "type": "boundary",
                "wikidata": "Q9928",
                "wikipedia": "nl:Heemstede (Noord-Holland)"
              },

    Coordinates: [[[x,y], [a,b]]]
    """

    log.debug(properties)

    # Verify that this doesn't exist yet to prevent double imports (when mistakes are made).
    if Organization.objects.all().filter(name=properties["name"],
                                         country=country,
                                         type__name=organization_type,
                                         is_dead=False).exists():
        return

    if "official_name" in properties:
        if Organization.objects.all().filter(name=properties["official_name"],
                                             country=country,
                                             type__name=organization_type,
                                             is_dead=False).exists():
            return

    # Prefer the official_name, as it usually looks nicer.
    name = properties["official_name"] if "official_name" in properties else properties["name"]

    new_organization = Organization(
        name=name,
        type=OrganizationType.objects.all().get(name=organization_type),
        country=country,
        created_on=when if when else datetime.now(pytz.utc),
        wikidata=properties["wikidata"] if "wikidata" in properties else "",
        wikipedia=properties["wikipedia"] if "wikipedia" in properties else "",
    )
    new_organization.save()  # has to be done in a separate call. can't append .save() to the organization object.
    log.info("Saved new organization: %s" % new_organization)

    new_coordinate = Coordinate(
        created_on=when if when else datetime.now(pytz.utc),
        organization=new_organization,
        creation_metadata="Automated import via OSM.",
        geojsontype=coordinates["type"],  # polygon or multipolygon
        area=coordinates["coordinates"]
    )
    new_coordinate.save()
    log.info("Saved new coordinate: %s" % new_coordinate)

    # try to find official urls for this organization, as it's empty now. All those will then be onboarded and scanned.
    if "wikidata" in properties:

        # validate that this region belongs to the right country
        # country = country, P17, you'll get a Q back
        # From the country get P297: ISO 3166-1 alpha-2 code
        country = ""
        isocode = ""

        website = ""
        try:
            client = Client()  # Q9928
            entity = client.get(properties["wikidata"], load=True)
            website = str(entity.get(client.get("P856"), None))  # P856 == Official Website.
            country = entity.get(client.get("P17"), None)
        except HTTPError:
            # No entity with ID Q15111448 was found... etc.
            # perfectly possible. In that case, no website, and thus continue.
            pass
        except Exception:
            # don't cause problems here... if the service is down, bad luck, try an import later etc...
            pass

        log.debug("Country: %s" % country)
        # validate country:
        if country:
            try:
                client = Client()  # Q9928
                entity = client.get(country.id, load=True)
                isocode = str(entity.get(client.get("P297"), None))
                log.debug("Retrieved ISO code: %s" % isocode)
            except HTTPError:
                # No entity with ID Q15111448 was found... etc.
                # perfectly possible. In that case, no website, and thus continue.
                pass
            except Exception:
                # don't cause problems here... if the service is down, bad luck, try an import later etc...
                pass

        log.debug("Matching isocode: %s", isocode)

        # instead of removing or breaking things, just update the organization to belong to this country.
        if isocode and new_organization.country != isocode.upper():
            log.info("The imported organization is from another country, saving it as such. This may cause some "
                     "issues as double organizations can be created.")
            new_organization.country = isocode.upper()
            new_organization.save()

        if not website or website == "None":
            return

        extract = tldextract.extract(website)

        if extract.subdomain:
            url = Url(url="%s.%s.%s" % (extract.subdomain, extract.domain, extract.suffix))
            url.save()
            url.organization.add(new_organization)
            url.save()
            log.info("Also found a subdomain website for this organization: %s" % website)

        # Even if it doesn't resolve directly, it is helpful for some scans:
        url = Url(url="%s.%s" % (extract.domain, extract.suffix))
        url.save()
        url.organization.add(new_organization)
        url.save()
        log.info("Also found a top level website for this organization: %s" % website)


def store_updates(feature: Dict, country: str = "NL", organization_type: str = "municipality", when=None):
    properties = feature["properties"]
    coordinates = feature["geometry"]

    """
    Handles the storing / administration of coordinates in failmap using the stacking pattern.

    "properties": {
                "@id": "relation/47394",
                "admin_level": "8",
                "authoritative": "yes",
                "boundary": "administrative",
                "name": "Heemstede",
                "ref:gemeentecode": "397",
                "source": "dataportal",
                "type": "boundary",
                "wikidata": "Q9928",
                "wikipedia": "nl:Heemstede (Noord-Holland)"
              },

    Coordinates: [[[x,y], [a,b]]]
    """
    # check if organization is part of the database
    # first try using it's OSM name
    matching_organization = None
    try:
        matching_organization = Organization.objects.get(name=properties["name"],
                                                         country=country,
                                                         type__name=organization_type,
                                                         is_dead=False)
    except Organization.DoesNotExist:
        log.debug("Could not find organization by property 'name', trying another way.")

    if not matching_organization and "official_name" in properties:
        try:
            matching_organization = Organization.objects.get(name=properties["official_name"],
                                                             country=country,
                                                             type__name=organization_type,
                                                             is_dead=False)
        except Organization.DoesNotExist:
            log.debug("Could not find organization by property 'official_name', trying another way.")

    if not matching_organization and "alt_name" in properties:
        try:
            matching_organization = Organization.objects.get(name=properties["alt_name"],
                                                             country=country,
                                                             type__name=organization_type,
                                                             is_dead=False)
        except Organization.DoesNotExist:
            log.debug("Could not find organization by property 'alt_name', trying another way.")

    if not matching_organization and "localname" in properties:
        try:
            matching_organization = Organization.objects.get(name=properties["localname"],
                                                             country=country,
                                                             type__name=organization_type,
                                                             is_dead=False)

        except Organization.DoesNotExist:
            # out of options...
            # This happens sometimes, as you might get areas that are outside the country or not on the map yet.
            log.debug("Could not find organization by property 'alt_name', we're out of options.")
            log.info("Organization from OSM does not exist in failmap, create it using the admin interface: '%s' "
                     "This might happen with neighboring countries (and the antilles for the Netherlands) or new "
                     "regions."
                     "If you are missing regions: did you create them in the admin interface or with an organization "
                     "merge script? Developers might experience this error using testdata etc.", properties["name"])
            log.info(properties)

    if not matching_organization:
        log.info("No matching organization found, no name, official_name or alt_name matches.")
        return

    # check if we're dealing with the right Feature:
    # if country == "NL" and organization_type == "municipality":
    #     if properties.get("boundary", "-") != "administrative":
    #         log.info("Feature did not contain properties matching this type of organization.")
    #         log.info("Missing boundary:administrative")
    #         return

    if not when:
        old_coordinate = Coordinate.objects.filter(organization=matching_organization, is_dead=False)
    else:
        old_coordinate = Coordinate.objects.filter(organization=matching_organization, is_dead=False,
                                                   created_on__lte=when)

    if old_coordinate.count() == 1 and old_coordinate[0].area == coordinates["coordinates"]:
        log.info("Retrieved coordinates are the same, not changing anything.")
        return

    message = ""

    if old_coordinate.count() > 1:
        message = "Automated import does not support multiple coordinates per organization. " \
                  "New coordinates will be created."

    if old_coordinate.count() == 1:
        message = "New data received in automated import."

        log.info(message)

    for old_coord in old_coordinate:
        old_coord.is_dead = True
        old_coord.is_dead_since = when if when else datetime.now(pytz.utc)
        old_coord.is_dead_reason = message
        old_coord.save()

    # Update the wikipedia references, given we have them now.
    if "wikidata" in coordinates or "wikipedia" in coordinates:
        matching_organization.wikidata = properties["wikidata"] if "wikidata" in properties else "",
        matching_organization.wikipedia = properties["wikipedia"] if "wikipedia" in properties else "",
        matching_organization.save()

    Coordinate(
        created_on=when if when else datetime.now(pytz.utc),
        organization=matching_organization,
        creation_metadata="Automated import via OSM.",
        geojsontype=coordinates["type"],  # polygon or multipolygon
        area=coordinates["coordinates"],
    ).save()

    log.info("Stored new coordinates!")


def get_osm_data_wambachers(country: str = "NL", organization_type: str = "municipality"):
    # uses https://wambachers-osm.website/boundaries/ to download map data. Might not be the most updated, but it has
    # a more complete and better set of queries. For example; it DOES get northern ireland and it clips out the sea,
    # which makes it very nice to look at.
    # yes, i've donated, and so should you :)
    """
    curl -f -o NL_province.zip 'https://wambachers-osm.website/boundaries/exportBoundaries
    ?cliVersion=1.0
    &cliKey=[key]  done: add cliKey to config
    &exportFormat=json
    &exportLayout=levels
    &exportAreas=land
    &union=false
    &from_al=4
    &to_al=4        done: get the right number
    &selected=NLD'  done: get 3 letter ISO code

    :param country:
    :param organization_type:
    :return:
    """

    # see if we cached a result
    filename = "%s_%s_%s.zip" % (re.sub(r'\W+', '', country), re.sub(r'\W+', '', organization_type),
                                 datetime.now(pytz.utc).date())
    filename = settings.TOOLS['openstreetmap']['output_dir'] + filename

    # if the file has been downloaded recently, don't do that again.
    four_hours_ago = time.time() - 14400
    if os.path.isfile(filename) and four_hours_ago < os.path.getmtime(filename):
        log.debug("Already downloaded a coordinate file in the past four hours. Using that one.")
        # unzip the file and return it's geojson contents.
        zip = zipfile.ZipFile(filename)
        files = zip.namelist()
        f = zip.open(files[0], 'r')
        contents = f.read()
        f.close()
        data = json.loads(contents)
        return data

    level = get_region(country, organization_type)
    country = countries.get(country)
    country_3_char_isocode = country.alpha3
    if not level:
        raise NotImplementedError(
            "Combination of country and organization_type does not have a matching OSM query implemented.")

    url = "https://wambachers-osm.website/boundaries/exportBoundaries?cliVersion=1.0&cliKey=%s&exportFormat=json" \
          "&exportLayout=levels&exportAreas=land&union=false&from_al=%s&to_al=%s&selected=%s" % (
              config.WAMBACHERS_OSM_CLIKEY, level, level, country_3_char_isocode)

    # get's a zip file and extract the content. The contents is the result. todo: Should be enough(?)
    response = requests.get(url, stream=True, timeout=(1200, 1200))
    response.raise_for_status()

    # show a nice progress bar when downloading
    with open(filename, 'wb') as f:
        for block in progress.bar(response.iter_content(chunk_size=1024), expected_size=(10240000 / 1024) + 1):
            if block:
                f.write(block)
                f.flush()

    # unzip the file and return it's geojson contents.
    zip = zipfile.ZipFile(filename)
    files = zip.namelist()
    f = zip.open(files[0], 'r')
    contents = f.read()
    f.close()
    data = json.loads(contents)
    return data


def get_osm_data(country: str = "NL", organization_type: str = "municipality"):
    """
    Runs an overpass query that results in a set with administrative borders and points with metadata.

    :return: dictionary
    """

    filename = "%s_%s_%s.osm" % (re.sub(r'\W+', '', country), re.sub(r'\W+', '', organization_type),
                                 datetime.now(pytz.utc).date())
    filename = settings.TOOLS['openstreetmap']['output_dir'] + filename

    # if the file has been downloaded recently, don't do that again.
    four_hours_ago = time.time() - 14400
    if os.path.isfile(filename + ".polygons") and four_hours_ago < os.path.getmtime(filename):
        log.debug("Already downloaded a coordinate file in the past four hours. Using that one.")
        log.debug(filename + ".polygons")
        return json.load(open(filename + ".polygons"))

    """
        The overpass query interface can be found here: https://overpass-turbo.eu/

        More on overpass can be found here: https://wiki.openstreetmap.org/wiki/Overpass_API

        The OSM file needs to be converted to paths etc.

        How administrative boundaries work, with a list of admin levels:
        https://wiki.openstreetmap.org/wiki/Tag:boundary=administrative
    """

    admin_level = get_region(country, organization_type)

    if not admin_level:
        raise NotImplementedError(
            "Combination of country and organization_type does not have a matching OSM query implemented.")

    # we used to use the country name, which doesn't work very consistently and requires a greater source of knowledge
    # luckily OSM supports ISO3166-2, just like django countries. So that's a perfect fit.
    query = 'area["ISO3166-2"~"^%s"]->.gem; relation(area.gem)[type=boundary]' \
            '[boundary=administrative][admin_level=%s]; out geom;' % (country, admin_level)

    log.info("Connecting to overpass to download data. Downloading can take a while (minutes)!")
    log.debug(query)
    response = requests.post("http://www.overpass-api.de/api/interpreter",
                             data={"data": query, "submit": "Query"},
                             stream=True,
                             timeout=(1200, 1200))

    response.raise_for_status()

    with open(filename, 'wb') as f:
        # total_length = int(response.headers.get('content-length'))
        # we don't get a content length from the api. So, "just" do something to show some progress...
        # {'Date': 'Tue, 20 Mar 2018 09:58:11 GMT', 'Server': 'Apache/2.4.18 (Ubuntu)', 'Vary': 'Accept-Encoding',
        # 'Content-Encoding': 'gzip', 'Keep-Alive': 'timeout=5, max=100', 'Connection': 'Keep-Alive',
        # 'Transfer-Encoding': 'chunked', 'Content-Type': 'application/osm3s+xml'}
        # overpass turbo does know this, probably _after_ downloading.
        # Assume 100 megabyte, NL = 40 MB. So give or take...
        for block in progress.bar(response.iter_content(chunk_size=1024), expected_size=(10240000 / 1024) + 1):
            if block:
                f.write(block)
                f.flush()

    log.info("Converting OSM file to polygons. This also can take a while...")
    try:
        with open(filename + ".polygons", "w") as outfile:
            subprocess.call(["osmtogeojson", filename], stdout=outfile)
    except subprocess.CalledProcessError:
        log.exception("Error while converting to polygons.")
    except OSError:
        log.exception("osmtogeojson tool not found.")

    return json.load(open(filename + ".polygons"))


def osmtogeojson_available():
    try:
        # todo: node --max_old_space_size=4000, for larger imprts... we don't even call node... :(
        subprocess.check_output(["osmtogeojson", "tesfile.osm"], stderr=subprocess.STDOUT, )
    except CalledProcessError as e:
        if "no such file or directory, open 'tesfile.osm'" in str(e.output):
            return True
        else:
            return False
    except FileNotFoundError:
        return False
