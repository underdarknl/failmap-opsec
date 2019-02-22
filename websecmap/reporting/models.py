from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField

from websecmap.organizations.models import Organization, Url


class SeriesOfUrlsReportMixin(models.Model):
    total_issues = models.IntegerField(help_text="The summed number of all vulnerabilities and failures.", default=0)
    high = models.IntegerField(help_text="The number of high risk vulnerabilities and failures.", default=0)
    medium = models.IntegerField(help_text="The number of medium risk vulnerabilities and failures.", default=0)
    low = models.IntegerField(help_text="The number of low risk vulnerabilities and failures.", default=0)

    total_urls = models.IntegerField(help_text="Amount of urls for this organization.", default=0)
    high_urls = models.IntegerField(help_text="Amount of urls with (1 or more) high risk issues.", default=0)
    medium_urls = models.IntegerField(help_text="Amount of urls with (1 or more) medium risk issues.", default=0)
    low_urls = models.IntegerField(help_text="Amount of urls with (1 or more) low risk issues.", default=0)

    total_endpoints = models.IntegerField(help_text="Amount of endpoints for this url.", default=0)
    high_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) high risk issues.", default=0)
    medium_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) medium risk issues.",
                                           default=0)
    low_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) low risk issues.", default=0)

    total_url_issues = models.IntegerField(help_text="Total amount of issues on url level.", default=0)
    url_issues_high = models.IntegerField(help_text="Number of high issues on url level.", default=0)
    url_issues_medium = models.IntegerField(help_text="Number of medium issues on url level.", default=0)
    url_issues_low = models.IntegerField(help_text="Number of low issues on url level.", default=0)

    total_endpoint_issues = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)
    endpoint_issues_high = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)
    endpoint_issues_medium = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)
    endpoint_issues_low = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)

    explained_total_issues = models.IntegerField(help_text="The summed number of all vulnerabilities and failures.",
                                                 default=0)
    explained_high = models.IntegerField(help_text="The number of high risk vulnerabilities and failures.", default=0)
    explained_medium = models.IntegerField(help_text="The number of medium risk vulnerabilities and failures.",
                                           default=0)
    explained_low = models.IntegerField(help_text="The number of low risk vulnerabilities and failures.", default=0)

    explained_total_urls = models.IntegerField(help_text="Amount of urls for this organization.", default=0)
    explained_high_urls = models.IntegerField(help_text="Amount of urls with (1 or more) high risk issues.", default=0)
    explained_medium_urls = models.IntegerField(help_text="Amount of urls with (1 or more) medium risk issues.",
                                                default=0)
    explained_low_urls = models.IntegerField(help_text="Amount of urls with (1 or more) low risk issues.", default=0)

    explained_total_endpoints = models.IntegerField(help_text="Amount of endpoints for this url.", default=0)
    explained_high_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) high risk issues.",
                                                   default=0)
    explained_medium_endpoints = models.IntegerField(
        help_text="Amount of endpoints with (1 or more) medium risk issues.", default=0)
    explained_low_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) low risk issues.",
                                                  default=0)

    explained_total_url_issues = models.IntegerField(help_text="Total amount of issues on url level.", default=0)
    explained_url_issues_high = models.IntegerField(help_text="Number of high issues on url level.", default=0)
    explained_url_issues_medium = models.IntegerField(help_text="Number of medium issues on url level.", default=0)
    explained_url_issues_low = models.IntegerField(help_text="Number of low issues on url level.", default=0)

    explained_total_endpoint_issues = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                          default=0)
    explained_endpoint_issues_high = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                         default=0)
    explained_endpoint_issues_medium = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                           default=0)
    explained_endpoint_issues_low = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                        default=0)

    when = models.DateTimeField(db_index=True)
    calculation = JSONField(
        help_text="Contains JSON with a calculation of all scanners at this moment, for all urls "
                  "of this organization. This can be a lot."
    )  # calculations of the independent urls... and perhaps others?

    def __str__(self):
        if any([self.high, self.medium, self.low]):
            return '🔴%s 🔶%s 🍋%s | %s' % (self.high, self.medium, self.low, self.when.date(),)
        else:
            return '✅ perfect | %s' % self.when.date()

    class Meta:
        abstract = True


class OrganizationReport(SeriesOfUrlsReportMixin):
    """
    This is basically an aggregation of UrlRating

    Contains aggregated ratings over time. Why?

    - Reduces complexity to get ratings
        You don't need to know about dead(urls, endpoints), scanner-results.
        For convenience purposes a calculation field also contains some hints why the rating is
        the way it is.

    -   It increases speed
        Instead of continuously calculating the score, it is done on a more regular interval: for
        example once every 10 minutes and only for the last 10 minutes.

    A time dimension is kept, since it's important to see what the rating was over time. This is
    now very simple to get (you don't need a complex join which is hard in django).

    The client software does a drill down on domains and shows why things are the way they are.
    Also this should not know too much about different scanners. In OO fashion, it should ask a
    scanner to explain why something is the way it is (over time).
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        get_latest_by = "when"
        index_together = [
            ["when", "id"],
        ]
        verbose_name = _('Organization Rating')
        verbose_name_plural = _('Organization Ratings')


class UrlReport(models.Model):
    """
        Aggregrates the results of many scanners to determine a rating for a URL.
    """
    url = models.ForeignKey(Url, on_delete=models.CASCADE)

    # cumulative issues on both the url and all underlying endpoints.
    total_issues = models.IntegerField(help_text="The summed number of all vulnerabilities and failures.", default=0)
    high = models.IntegerField(help_text="The number of high risk vulnerabilities and failures.", default=0)
    medium = models.IntegerField(help_text="The number of medium risk vulnerabilities and failures.", default=0)
    low = models.IntegerField(help_text="The number of low risk vulnerabilities and failures.", default=0)

    # How much % of endpoints has issues per level
    total_endpoints = models.IntegerField(help_text="Amount of endpoints for this url.", default=0)
    high_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) high risk issues.", default=0)
    medium_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) medium risk issues.",
                                           default=0)
    low_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) low risk issues.", default=0)

    total_url_issues = models.IntegerField(help_text="Total amount of issues on url level.", default=0)
    url_issues_high = models.IntegerField(help_text="Number of high issues on url level.", default=0)
    url_issues_medium = models.IntegerField(help_text="Number of medium issues on url level.", default=0)
    url_issues_low = models.IntegerField(help_text="Number of low issues on url level.", default=0)

    total_endpoint_issues = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)
    endpoint_issues_high = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)
    endpoint_issues_medium = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)
    endpoint_issues_low = models.IntegerField(help_text="Total amount of issues on endpoint level.", default=0)

    # Complay or explain
    explained_total_issues = models.IntegerField(help_text="The summed number of all vulnerabilities and failures.",
                                                 default=0)
    explained_high = models.IntegerField(help_text="The number of high risk vulnerabilities and failures.", default=0)
    explained_medium = models.IntegerField(help_text="The number of medium risk vulnerabilities and failures.",
                                           default=0)
    explained_low = models.IntegerField(help_text="The number of low risk vulnerabilities and failures.", default=0)

    explained_total_endpoints = models.IntegerField(help_text="Amount of endpoints for this url.", default=0)
    explained_high_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) high risk issues.",
                                                   default=0)
    explained_medium_endpoints = models.IntegerField(
        help_text="Amount of endpoints with (1 or more) medium risk issues.",
        default=0)
    explained_low_endpoints = models.IntegerField(help_text="Amount of endpoints with (1 or more) low risk issues.",
                                                  default=0)

    explained_total_url_issues = models.IntegerField(help_text="Total amount of issues on url level.", default=0)
    explained_url_issues_high = models.IntegerField(help_text="Number of high issues on url level.", default=0)
    explained_url_issues_medium = models.IntegerField(help_text="Number of medium issues on url level.", default=0)
    explained_url_issues_low = models.IntegerField(help_text="Number of low issues on url level.", default=0)

    explained_total_endpoint_issues = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                          default=0)
    explained_endpoint_issues_high = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                         default=0)
    explained_endpoint_issues_medium = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                           default=0)
    explained_endpoint_issues_low = models.IntegerField(help_text="Total amount of issues on endpoint level.",
                                                        default=0)

    when = models.DateTimeField(db_index=True)

    calculation = JSONField(
        help_text="Contains JSON with a calculation of all scanners at this moment. The rating can "
                  "be spread out over multiple endpoints, which might look a bit confusing. Yet it "
                  "is perfectly possible as some urls change their IP every five minutes and "
                  "scans are spread out over days."
    )

    class Meta:
        managed = True
        verbose_name = _('Url Rating')
        verbose_name_plural = _('Url Ratings')

    def __str__(self):
        return '%s,%s,%s  - %s' % (self.high, self.medium, self.low, self.when.date(),)

# todo: we can make a vulnerabilitystatistic per organization type or per tag. But not per country, list etc.
