import logging

from django.core.management.base import BaseCommand

from websecmap.organizations.models import Url
from websecmap.reporting.report import create_timeline, inspect_timeline

log = logging.getLogger(__package__)


class Command(BaseCommand):
    help = "Shows timeline of a certain URL"

    def add_arguments(self, parser):
        """Add command specific arguments."""

        parser.add_argument("-u", "--url_addresses", nargs="*")

    def handle(self, *args, **options):

        if not options["url_addresses"]:
            print("Specify url using -u. timeline -u example.com")
            exit()

        # create a case-insensitive filter to match organizations by name
        regex = "^(" + "|".join(options["url_addresses"]) + ")$"

        urls = Url.objects.all().filter(url__iregex=regex, is_dead=False)

        for url in urls:
            print(inspect_timeline(create_timeline(url), url))
