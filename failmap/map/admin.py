from adminsortable2.admin import SortableAdminMixin
from celery import group
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from failmap.app.models import Job
from failmap.celery import PRIO_HIGH, app
from failmap.map.geojson import import_from_scratch, update_coordinates
from failmap.map import models
import logging

log = logging.getLogger(__package__)


@admin.register(models.OrganizationRating)
class OrganizationRatingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def inspect_organization(self, obj):
        return format_html(
            '<a href="../../organizations/organization/{id}/change">inspect organization</a>',
            id=format(obj.organization_id))

    list_display = ('organization', 'total_urls', 'total_endpoints', 'report', 'explained_high', 'explained_medium',
                    'explained_low', 'when', 'inspect_organization')
    search_fields = (['organization__name', 'when'])
    list_filter = ['organization', 'organization__country', 'organization__type__name', 'when'][::-1]
    # fields = [field.name for field in OrganizationRating._meta.get_fields() if field.name != "id"][::-1]

    fields = ('organization', 'total_urls', 'total_endpoints',
              'high',
              'medium',
              'low',
              'high_urls',
              'medium_urls',
              'low_urls',
              'high_endpoints',
              'medium_endpoints',
              'low_endpoints',
              'total_url_issues',
              'url_issues_high',
              'url_issues_medium',
              'url_issues_low',
              'total_endpoint_issues',
              'endpoint_issues_high',
              'endpoint_issues_medium',
              'endpoint_issues_low',
              'explained_high',
              'explained_medium',
              'explained_low',
              'explained_high_urls',
              'explained_medium_urls',
              'explained_low_urls',
              'explained_high_endpoints',
              'explained_medium_endpoints',
              'explained_low_endpoints',
              'explained_total_url_issues',
              'explained_url_issues_high',
              'explained_url_issues_medium',
              'explained_url_issues_low',
              'explained_total_endpoint_issues',
              'explained_endpoint_issues_high',
              'explained_endpoint_issues_medium',
              'explained_endpoint_issues_low',
              'when',
              'calculation')

    def report(self, obj):
        return obj

    ordering = ["-when"]

    save_as = True


@admin.register(models.UrlRating)
class UrlRatingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def inspect_url(self, obj):
        return format_html('<a href="../../organizations/url/{id}/change">inspect</a>',
                           id=format(obj.url_id))

    list_display = ('url', 'high', 'medium', 'low', 'total_endpoints', 'when', 'inspect_url')
    search_fields = (['url__organization__name', 'url__url', 'when'])
    list_filter = ['url', 'when', 'url__organization__type', 'url__organization__country'][::-1]
    fields = ('url', 'total_endpoints',
              'total_issues',

              'high',
              'medium',
              'low',
              'high_endpoints',
              'medium_endpoints',
              'low_endpoints',
              'total_url_issues',
              'url_issues_high',
              'url_issues_medium',
              'url_issues_low',
              'total_endpoint_issues',
              'endpoint_issues_high',
              'endpoint_issues_medium',
              'endpoint_issues_low',

              'explained_high',
              'explained_medium',
              'explained_low',
              'explained_high_endpoints',
              'explained_medium_endpoints',
              'explained_low_endpoints',
              'explained_total_url_issues',
              'explained_url_issues_high',
              'explained_url_issues_medium',
              'explained_url_issues_low',
              'explained_total_endpoint_issues',
              'explained_endpoint_issues_high',
              'explained_endpoint_issues_medium',
              'explained_endpoint_issues_low',

              'when', 'calculation')

    ordering = ["-when"]

    save_as = True


@admin.register(models.AdministrativeRegion)
class AdministrativeRegionAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('country', 'organization_type', 'admin_level', 'imported', 'resampling_resolution')
    search_fields = (['country', 'organization_type', 'admin_level'])
    list_filter = ['country', 'organization_type', 'admin_level', 'imported'][::-1]
    fields = ('country', 'organization_type', 'admin_level', 'imported', 'resampling_resolution')

    actions = []

    def import_region(self, request, queryset):
        tasks = []

        for region in queryset:
            tasks.append(import_from_scratch.s([str(region.country)], [region.organization_type.name])
                         | add_configuration.si(region.country, region.organization_type)
                         | set_imported.si(region))

        task_name = "%s (%s) " % ("Import region", ','.join(map(str, list(queryset))))
        task = group(tasks)

        job = Job.create(task, task_name, request, priority=PRIO_HIGH)
        link = reverse('admin:app_job_change', args=(job.id,))
        self.message_user(request, 'Job created, <a href="%s">%s</a>' % (link, task_name))

    import_region.short_description = '🛃  Import region'
    actions.append(import_region)

    # ah, hmm... abstractions...
    # something something abstractions
    def update_coordinates(self, request, queryset):
        tasks = []

        for region in queryset:
            tasks.append(update_coordinates.s([str(region.country)], [region.organization_type.name]))

        task_name = "%s (%s) " % ("Update region", ','.join(map(str, list(queryset))))
        task = group(tasks)

        job = Job.create(task, task_name, request, priority=PRIO_HIGH)
        link = reverse('admin:app_job_change', args=(job.id,))
        self.message_user(request, 'Job created, <a href="%s">%s</a>' % (link, task_name))
    update_coordinates.short_description = '🛂  Update region'
    actions.append(update_coordinates)


@app.task(queue='storage')
def set_imported(region: models.AdministrativeRegion):
    region.imported = True
    region.save()


@app.task(queue='storage')
def add_configuration(country, organization_type):

    if models.Configuration.objects.all().filter(country=country, organization_type=organization_type).exists():
        log.debug("This configuration already exists, skipping.")
        return

    a = models.Configuration(
        country=country,
        organization_type=organization_type,
        is_the_default_option=False,
        is_displayed=False,
        is_scanned=False
    )
    a.save()


@admin.register(models.Configuration)
class ConfigurationAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ('country', 'organization_type', 'is_displayed', 'is_the_default_option', 'is_scanned',
                    'is_reported')
    search_fields = (['country', 'organization_type', ])
    list_filter = ['country', 'organization_type', 'is_displayed', 'is_the_default_option',
                   'is_scanned', 'is_reported'][::-1]
    fields = ('country', 'organization_type', 'is_displayed', 'is_the_default_option', 'is_scanned', 'is_reported')

    actions = []

    def display(self, request, queryset):

        for configuration in queryset:
            configuration.is_displayed = True
            configuration.save()

    display.short_description = '☀️ Display'
    actions.append(display)

    def hide(self, request, queryset):

        for configuration in queryset:
            configuration.is_displayed = False
            configuration.save()

    hide.short_description = '🌑 Hide'
    actions.append(hide)

    def allow_scanning(self, request, queryset):

        for configuration in queryset:
            configuration.is_scanned = True
            configuration.save()

    allow_scanning.short_description = '❤️  Allow scanning'
    actions.append(allow_scanning)

    def stop_scanning(self, request, queryset):

        for configuration in queryset:
            configuration.is_scanned = False
            configuration.save()

    stop_scanning.short_description = '💔  Stop scanning'
    actions.append(stop_scanning)

    def allow_reporting(self, request, queryset):

        for configuration in queryset:
            configuration.is_reported = True
            configuration.save()

    allow_reporting.short_description = '📄️  Allow Reporting'
    actions.append(allow_reporting)

    def stop_reporting(self, request, queryset):

        for configuration in queryset:
            configuration.is_reported = False
            configuration.save()

    stop_reporting.short_description = '📄  Stop Reporting'
    actions.append(stop_reporting)

    def create_report(self, request, queryset):

        for configuration in queryset:

            from failmap.map.report import compose_task

            organization_filter = {'country': configuration.country,
                                   'type': configuration.organization_type}

            task = compose_task(organizations_filter=organization_filter)
            task.apply_async()

        self.message_user(request, 'Reports are being generated in the background.')

    create_report.short_description = '📄  Report'
    actions.append(create_report)

    def set_default(self, request, queryset):

        for configuration in queryset:
            configuration.is_the_default_option = True
            configuration.save()

    set_default.short_description = '😀  Set default'
    actions.append(set_default)

    def remove_default(self, request, queryset):

        for configuration in queryset:
            configuration.is_the_default_option = False
            configuration.save()

    remove_default.short_description = '😭  Remove default'
    actions.append(remove_default)


@admin.register(models.VulnerabilityStatistic)
class VulnerabilityStatisticAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('country', 'organization_type', 'scan_type', 'when', 'high', 'medium', 'low', 'urls', 'endpoints')
    list_filter = ['country', 'organization_type', 'scan_type', 'when', 'high', 'medium', 'low'][::-1]
    search_fields = (['country', 'organization_type', 'scan_type'])


@admin.register(models.MapDataCache)
class MapDataCacheAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('pk', 'country', 'organization_type', 'filters', 'when')
    list_filter = ['country', 'organization_type', 'filters', 'when'][::-1]
    search_fields = (['country', 'organization_type', 'filters'])

    readonly_fields = ['cached_on']

    @staticmethod
    def length(obj):
        # retrieving this causes a massive slowdown on getting the dataset
        return len(str(obj.dataset))
