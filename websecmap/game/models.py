from colorful.fields import RGBColorField
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from websecmap.organizations.models import Organization, Url

# Highest level adding:

# We're going to match things that exist already, we're not going to code an entire admin interface?


class Contest(models.Model):
    name = models.CharField(
        verbose_name=_("Contest name"),
        max_length=42,
        help_text="Name of the contest, might be abbreviated, don't use long words.",
    )

    from_moment = models.DateTimeField(blank=True, null=True, help_text="Moment the compo opens.")

    until_moment = models.DateTimeField(blank=True, null=True, help_text="Moment the compo closes.")

    target_country = CountryField(help_text="The country (if any) under which submissions fall.")

    url_organization_discovery_help = models.TextField(
        max_length=1024,
        default="",
        help_text="HTML: information where contestants can find good sources of urls / organizations. Displayed on"
        " both the URL and Organization adding forms.",
        blank=True,
        null=True,
    )

    admin_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("contest")
        verbose_name_plural = _("contests")

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    """
    These are managed by the admin interface in the first version.

    """

    name = models.CharField(
        verbose_name=_("Team name"), max_length=42, help_text="Whatever name the team wants. Must be at least PEGI 88."
    )

    secret = models.CharField(
        max_length=42, help_text="A secret that allows them to add URLS under their team (for scoring purposes)"
    )

    participating_in_contest = models.ForeignKey(Contest, null=True, blank=True, on_delete=models.CASCADE)

    color = RGBColorField(
        colors=[
            "#F2D7D5",
            "#FADBD8",
            "#EBDEF0",
            "#E8DAEF",
            "#D4E6F1",
            "#D6EAF8",
            "#D1F2EB",
            "#D0ECE7",
            "#D4EFDF",
            "#D5F5E3",
            "#FCF3CF",
            "#FDEBD0",
            "#FAE5D3",
            "#F6DDCC",
        ],
        null=True,
        blank=True,
    )

    allowed_to_submit_things = models.BooleanField(default=False, help_text="Disables teams from submitting things.")

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __str__(self):
        return mark_safe(
            f"{self.participating_in_contest}/<span style='background-color: {self.color}'>{self.name}</span>"
        )


class OrganizationSubmission(models.Model):

    organization_country = CountryField()

    added_by_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    # Organization types are managed by the admin, so informed decisions are made.
    # the type is not really important, that will be managed anyway. It's more a suggestion.
    organization_type_name = models.CharField(
        max_length=42, default="unknown", help_text="The contest the team is participating in."
    )

    # the name should translate to the natural key of an existing (or a new) organization.
    # organizations can be created in the admin interface
    organization_name = models.CharField(
        max_length=250, default="unknown", help_text="The contest the team is participating in."
    )

    organization_address = models.CharField(
        max_length=600,
        default="unknown",
        help_text="The address of the (main location) of the organization. This will be used for geocoding.",
    )

    organization_evidence = models.CharField(
        max_length=600, default="unknown", help_text="Sources of information about this organization."
    )

    # geojsonfields require the type defined in the geojson. We don't store geojson but just a coordinate.
    organization_address_geocoded = models.CharField(
        max_length=5000, null=True, blank=True, help_text="Automatic geocoded organization address."
    )

    organization_wikipedia = models.URLField(
        null=True, blank=True, help_text="Helps finding more info about the organization."
    )

    organization_wikidata_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="The code for this page that starts with Q. Search for wikidata and the terms you're looking for to"
        " get this code.",
    )

    organization_in_system = models.ForeignKey(
        Organization,
        null=True,
        help_text="This reference will be used to calculate the score and to track imports.",
        blank=True,
        on_delete=models.CASCADE,
    )

    has_been_accepted = models.BooleanField(
        default=False,
        help_text="If the admin likes it, they can accept the submission to be part of the real system",
        db_index=True,
    )

    has_been_rejected = models.BooleanField(
        default=False, help_text="Nonsense organizations can be rejected.", db_index=True
    )

    added_on = models.DateTimeField(
        blank=True, null=True, help_text="Automatically filled when creating a new submission."
    )

    suggested_urls = models.TextField(
        help_text="A set of or urls, comma separated that can be added when the organization was approved.",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.has_been_accepted:
            return f"OK: {self.organization_name}"
        else:
            return self.organization_name

    class Meta:
        verbose_name = _("organisation submission")
        verbose_name_plural = _("organisation submissions")


class UrlSubmission(models.Model):
    """
    Submissions are suggestions of urls to add. They are not directly added to the system.
    The admin of the system is the consensus algorithm.

    The admin can do "imports" on these submissions if they think it's a good one.
    Todo: create admin action.

    """

    added_by_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)

    for_organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)

    url = models.CharField(max_length=500, help_text="The URL the team has submitted, for review before acceptance.")

    url_in_system = models.ForeignKey(
        Url,
        null=True,
        help_text="This reference will be used to calculate the score and to track imports.",
        blank=True,
        on_delete=models.CASCADE,
    )

    has_been_accepted = models.BooleanField(
        default=False,
        help_text="If the admin likes it, they can accept the submission to be part of the real system",
        db_index=True,
    )

    has_been_rejected = models.BooleanField(
        default=False, help_text="Rejected urls makes for deduction in points.", db_index=True
    )

    added_on = models.DateTimeField(
        blank=True, null=True, help_text="Automatically filled when creating a new submission."
    )

    def __str__(self):
        if self.has_been_accepted:
            return f"OK: {self.url}"
        else:
            return self.url

    class Meta:
        verbose_name = _("url submission")
        verbose_name_plural = _("url submissions")
