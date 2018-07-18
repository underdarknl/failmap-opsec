"""
Check if a domain is only reachable on plain http, instead of both http and https.

Browsers first connect to http, not https when entering a domain. That will be changed in the future.

Further reading:
https://stackoverflow.com/questions/20475552/python-requests-library-redirect-new-url#20475712
"""
import logging

from celery import Task, group

from failmap.organizations.models import Organization, Url
from failmap.scanners.endpoint_scan_manager import EndpointScanManager
from failmap.scanners.scanner_http import (redirects_to_safety, resolve_and_scan_tasks,
                                           resolves_on_v4, resolves_on_v6)

from ..celery import app
from .models import Endpoint
from .scanner import allowed_to_scan, q_configurations_to_scan

log = logging.getLogger(__package__)


def compose_task(
    organizations_filter: dict = dict(),
    urls_filter: dict = dict(),
    endpoints_filter: dict = dict(),
) -> Task:
    """Compose taskset to scan specified endpoints.

    *This is an implementation of `compose_task`. For more documentation about this concept, arguments and concrete
    examples of usage refer to `compose_task` in `types.py`.*

    """

    # We might not be allowed to scan for this at all.
    if not allowed_to_scan("scanner_plain_http"):
        return group()  # An empty group fits this callable's signature and does not impede celery.

    if organizations_filter:
        organizations = Organization.objects.filter(is_dead=False, **organizations_filter)
        urls = Url.objects.filter(q_configurations_to_scan(),
                                  organization__in=organizations, is_dead=False, not_resolvable=False, **urls_filter)
        log.info('Creating scan task %s urls for %s organizations.', len(urls), len(organizations))
    else:
        urls = Url.objects.filter(q_configurations_to_scan(), is_dead=False, not_resolvable=False, **urls_filter)
        log.info('Creating scan plain http task %s urls.', len(urls))

    if endpoints_filter:
        raise NotImplementedError('This scanner needs to be refactored to scan per endpoint.')

    if not urls:
        log.warning('Applied filters resulted in no urls, thus no tasks!')
        return group()

    # create tasks for scanning all selected endpoints as a single managable group
    task = group(scan_url.s(url) for url in urls)

    return task


# This needs to be refactored to move the Endpoint iteration to `compose_task`
# and split this task up in a scan and store task so scans can be performed more
# distributed. For examples see scan_dummy.py

# http://185.3.211.120:80: Host: demo3.data.amsterdam.nl Status: 301
@app.task(queue='storage')
def scan_url(url: Url):
    """

    :param url:
    :return:
    """

    # todo: verify that the you have both ipv4 6 and ipv6 capabilities.

    log.info("started scanning url %s" % url)

    tasks = []

    scan_manager = EndpointScanManager
    log.debug("Checking for http only sites on: %s" % url)
    endpoints = Endpoint.objects.all().filter(url=url, is_dead=False)

    has_http_v4 = False
    has_https_v4 = False
    has_http_v6 = False
    has_https_v6 = False
    http_v4_endpoint = None
    http_v6_endpoint = None

    cleaned_up = "Has a secure equivalent, which wasn't so in the past."
    not_resolvable_at_all = "Cannot be resolved anymore, seems to be cleaned up."

    # The default ports matter for normal humans. All services on other ports are special services.
    # we only give points if there is not a normal https site when there is a normal http site.

    for endpoint in endpoints:
        if endpoint.protocol == "http" and endpoint.port == 80 and endpoint.ip_version == 4:
            has_http_v4 = True
            http_v4_endpoint = endpoint
        if endpoint.protocol == "https" and endpoint.port == 443 and endpoint.ip_version == 4:
            has_https_v4 = True

        if endpoint.protocol == "http" and endpoint.port == 80 and endpoint.ip_version == 6:
            has_http_v6 = True
            http_v6_endpoint = endpoint

        if endpoint.protocol == "https" and endpoint.port == 443 and endpoint.ip_version == 6:
            has_https_v6 = True

    # calculate the score
    # Organizations with wildcards can have this problem a lot:
    # 1: It's not possible to distinguish the default page with another page, wildcards
    #    can help hide domains and services.
    # 2: A wildcard TLS connection is an option: then it will be fine, and it can be also
    #    run only on everything that is NOT another service on the server: also hiding stuff
    # 3: Due to SNI it's not possible where something is served.

    # !!! The only solution is to have a "curated" list of port 80 websites. !!!
    # maybe compare an image of a non existing url with the random ones given here.
    # if they are the same, then there is really no site. That should help clean
    # non-existing wildcard domains.

    # Comparing with screenshots is simply not effective enough:
    # 1: Many HTTPS sites load HTTP resources, which don't show, and thus it's different.
    # 2: There is no guarantee that a wildcard serves a blank page.
    # 3: In the transition phase to default https (coming years), it's not possible to say
    #    what should be the "leading" site.

    # Some organizations redirect the http site to a non-standard https port.
    # occurs more than once... you still have to follow redirects?
    if has_http_v4 and not has_https_v4:
        log.debug("Needs to check ipv4")
        # fixing https://sentry.io/internet-cleanup-foundation/faalkaart/issues/435116126/
        if not resolves_on_v4(url.url):
            # the endpoint scanner will probably find there is no endpoint anymore as well...
            log.debug("Does not resolve at all, so has no insecure endpoints. %s" % url)
            scan_manager.add_scan("plain_https", http_v4_endpoint, "0", not_resolvable_at_all)
        else:
            log.debug("This url seems to have no https at all: %s" % url)
            log.debug("Checking if they exist, to be sure there is nothing.")

            tasks.append(resolve_and_scan_tasks('https', url, 443)
                         | handle_verify_is_secure.si(http_v4_endpoint, url))

    else:
        # it is secure, and if there was a rating, then reduce it to 0 (with a new rating).
        log.debug("We don't have to do anything for v4 on %s" % url)
        if scan_manager.had_scan_with_points("plain_https", http_v4_endpoint):
            scan_manager.add_scan("plain_https", http_v4_endpoint, "0", cleaned_up)

    if has_http_v6 and not has_https_v6:
        log.debug("Needs to check ipv6")
        if not resolves_on_v6(url.url):
            log.debug("Does not resolve at all, so has no insecure endpoints. %s" % url)
            scan_manager.add_scan("plain_https", http_v6_endpoint, "0", not_resolvable_at_all)
        else:
            tasks.append(
                (resolve_and_scan_tasks('https', url, 443) | handle_verify_is_secure.si(http_v6_endpoint, url)))

    else:
        log.debug("We don't have to do anything for v6 on %s" % url)
        if scan_manager.had_scan_with_points("plain_https", http_v6_endpoint):
            scan_manager.add_scan("plain_https", http_v6_endpoint, "0", cleaned_up)

    task = group(tasks)
    if task:
        log.info("Task chain: %s" % task)
        task.apply_async()


# unfortunately due to my limited experience with tasks, i've placed this on the storage queue so there is
# direct access to the database and performing a scan.
@app.task(queue="storage")
def handle_verify_is_secure(endpoint, url):

    secure_endpoints = Endpoint.objects.all().filter(
        url=endpoint.url,
        is_dead=False,
        protocol="https",
        port=443,
        ip_version=endpoint.ip_version)

    saved_by_the_bell = "Redirects to a secure site, while a secure counterpart on the standard port is missing."
    no_https_at_all = "Site does not redirect to secure url, and has no secure alternative on a standard port."

    if not secure_endpoints:
        log.info("Checking if the URL redirects to a secure url: %s" % url)
        if redirects_to_safety(endpoint):
            log.info("%s redirects to safety, saved by the bell." % url)
            EndpointScanManager.add_scan("plain_https", endpoint, "25", saved_by_the_bell)

        else:
            log.info("%s does not have a https site. Saving/updating scan." % url)
            EndpointScanManager.add_scan("plain_https", endpoint, "1000", no_https_at_all)
