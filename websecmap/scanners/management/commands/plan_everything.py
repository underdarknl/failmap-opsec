import logging

from django.core.management.base import BaseCommand

from websecmap.scanners.scanner import (
    dns_endpoints,
    dns_known_subdomains,
    dns_wildcards,
    dnssec,
    ftp,
    http,
    internet_nl_v2_mail,
    internet_nl_v2_web,
    plain_http,
    security_headers,
    subdomains,
    tls_qualys,
    verify_unresolvable,
)

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Normally all scans are planned and executed using periodic tasks. This command however will plan
    all verify, discovery and scan tasks on the entire system.
    """

    def handle(self, *args, **options):
        # internet.nl v2 scanner has to be used in websecmap.
        for scanner in [
            ftp,
            dnssec,
            security_headers,
            tls_qualys,
            plain_http,
            subdomains,
            dns_wildcards,
            dns_known_subdomains,
            dns_endpoints,
            http,
            internet_nl_v2_mail,
            internet_nl_v2_web,
            verify_unresolvable,
        ]:
            for planning_method in ["plan_discover", "plan_verify", "plan_scan"]:
                method = getattr(scanner, planning_method, None)
                if method:
                    method()
