import logging
from argparse import ArgumentTypeError
from datetime import datetime

from django.core.management.base import BaseCommand

from websecmap.map.logic.openstreetmap import import_from_scratch
from websecmap.map.models import AdministrativeRegion

log = logging.getLogger(__package__)


class Command(BaseCommand):
    help = (
        "Connects to OSM and gets a set of coordinates. Example:"
        "failmap import_coordinates --country=SE --region=municipality --date=2018-01-01"
    )

    # NL, province: failmap import_coordinates --country=NL --region=province --date=2018-01-01
    # LU, all: failmap import_coordinates --country=LU --date=2018-01-01
    # all, all... which you don't want(!) :) : failmap import_coordinates --date=2018-01-01

    def add_arguments(self, parser):

        parser.add_argument("--country", help="Country code. Eg: NL, DE, EN", required=False)

        parser.add_argument("--region", help="Region: municipality, province, water\ board ...", required=False)

        parser.add_argument(
            "--date",
            help="Date since when the import should be effective. - format YYYY-MM-DD",
            required=False,
            type=valid_date,
        )

        parser.add_argument(
            "--list", help="Lists the currently available regions and countries.", required=False, action="store_true"
        )

    # https://nl.wikipedia.org/wiki/Gemeentelijke_herindelingen_in_Nederland#Komende_herindelingen
    def handle(self, *app_labels, **options):

        if options["list"]:
            log.info("Currently available administrative regions:")
            log.info("Hint: add the via the admin interface.")
            x = AdministrativeRegion.objects.all()
            if not x:
                log.info("-- None found. Add them via the admin interface.")

            for z in x:
                log.info("%-3s %-72s, %-5s" % (z.country, z.organization_type, z.admin_level))

        else:
            import_from_scratch(
                countries=[options["country"]], organization_types=[options["region"]], when=options["date"]
            )


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)
