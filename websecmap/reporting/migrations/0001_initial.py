# Generated by Django 2.1.7 on 2019-02-22 10:40

import django.db.models.deletion
import django_countries.fields
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("organizations", "0053_url_do_not_find_subdomains"), ("map", "0041_auto_20190222_1036")]

    state_operations = [
        migrations.CreateModel(
            name="OrganizationReport",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "total_issues",
                    models.IntegerField(default=0, help_text="The summed number of all vulnerabilities and failures."),
                ),
                (
                    "high",
                    models.IntegerField(default=0, help_text="The number of high risk vulnerabilities and failures."),
                ),
                (
                    "medium",
                    models.IntegerField(default=0, help_text="The number of medium risk vulnerabilities and failures."),
                ),
                (
                    "low",
                    models.IntegerField(default=0, help_text="The number of low risk vulnerabilities and failures."),
                ),
                ("total_urls", models.IntegerField(default=0, help_text="Amount of urls for this organization.")),
                (
                    "high_urls",
                    models.IntegerField(default=0, help_text="Amount of urls with (1 or more) high risk issues."),
                ),
                (
                    "medium_urls",
                    models.IntegerField(default=0, help_text="Amount of urls with (1 or more) medium risk issues."),
                ),
                (
                    "low_urls",
                    models.IntegerField(default=0, help_text="Amount of urls with (1 or more) low risk issues."),
                ),
                ("total_endpoints", models.IntegerField(default=0, help_text="Amount of endpoints for this url.")),
                (
                    "high_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) high risk issues."),
                ),
                (
                    "medium_endpoints",
                    models.IntegerField(
                        default=0, help_text="Amount of endpoints with (1 or more) medium risk issues."
                    ),
                ),
                (
                    "low_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) low risk issues."),
                ),
                ("total_url_issues", models.IntegerField(default=0, help_text="Total amount of issues on url level.")),
                ("url_issues_high", models.IntegerField(default=0, help_text="Number of high issues on url level.")),
                (
                    "url_issues_medium",
                    models.IntegerField(default=0, help_text="Number of medium issues on url level."),
                ),
                ("url_issues_low", models.IntegerField(default=0, help_text="Number of low issues on url level.")),
                (
                    "total_endpoint_issues",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "endpoint_issues_high",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "endpoint_issues_medium",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "endpoint_issues_low",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_total_issues",
                    models.IntegerField(default=0, help_text="The summed number of all vulnerabilities and failures."),
                ),
                (
                    "explained_high",
                    models.IntegerField(default=0, help_text="The number of high risk vulnerabilities and failures."),
                ),
                (
                    "explained_medium",
                    models.IntegerField(default=0, help_text="The number of medium risk vulnerabilities and failures."),
                ),
                (
                    "explained_low",
                    models.IntegerField(default=0, help_text="The number of low risk vulnerabilities and failures."),
                ),
                (
                    "explained_total_urls",
                    models.IntegerField(default=0, help_text="Amount of urls for this organization."),
                ),
                (
                    "explained_high_urls",
                    models.IntegerField(default=0, help_text="Amount of urls with (1 or more) high risk issues."),
                ),
                (
                    "explained_medium_urls",
                    models.IntegerField(default=0, help_text="Amount of urls with (1 or more) medium risk issues."),
                ),
                (
                    "explained_low_urls",
                    models.IntegerField(default=0, help_text="Amount of urls with (1 or more) low risk issues."),
                ),
                (
                    "explained_total_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints for this url."),
                ),
                (
                    "explained_high_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) high risk issues."),
                ),
                (
                    "explained_medium_endpoints",
                    models.IntegerField(
                        default=0, help_text="Amount of endpoints with (1 or more) medium risk issues."
                    ),
                ),
                (
                    "explained_low_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) low risk issues."),
                ),
                (
                    "explained_total_url_issues",
                    models.IntegerField(default=0, help_text="Total amount of issues on url level."),
                ),
                (
                    "explained_url_issues_high",
                    models.IntegerField(default=0, help_text="Number of high issues on url level."),
                ),
                (
                    "explained_url_issues_medium",
                    models.IntegerField(default=0, help_text="Number of medium issues on url level."),
                ),
                (
                    "explained_url_issues_low",
                    models.IntegerField(default=0, help_text="Number of low issues on url level."),
                ),
                (
                    "explained_total_endpoint_issues",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_endpoint_issues_high",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_endpoint_issues_medium",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_endpoint_issues_low",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                ("when", models.DateTimeField(db_index=True)),
                (
                    "calculation",
                    jsonfield.fields.JSONField(
                        help_text="Contains JSON with a calculation of all scanners at this moment, for all urls of this organization. This can be a lot."
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.Organization"),
                ),
            ],
            options={
                "verbose_name": "Organization Rating",
                "verbose_name_plural": "Organization Ratings",
                "db_table": "map_organizationreport",
                "get_latest_by": "when",
            },
        ),
        migrations.CreateModel(
            name="UrlReport",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "total_issues",
                    models.IntegerField(default=0, help_text="The summed number of all vulnerabilities and failures."),
                ),
                (
                    "high",
                    models.IntegerField(default=0, help_text="The number of high risk vulnerabilities and failures."),
                ),
                (
                    "medium",
                    models.IntegerField(default=0, help_text="The number of medium risk vulnerabilities and failures."),
                ),
                (
                    "low",
                    models.IntegerField(default=0, help_text="The number of low risk vulnerabilities and failures."),
                ),
                ("total_endpoints", models.IntegerField(default=0, help_text="Amount of endpoints for this url.")),
                (
                    "high_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) high risk issues."),
                ),
                (
                    "medium_endpoints",
                    models.IntegerField(
                        default=0, help_text="Amount of endpoints with (1 or more) medium risk issues."
                    ),
                ),
                (
                    "low_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) low risk issues."),
                ),
                ("total_url_issues", models.IntegerField(default=0, help_text="Total amount of issues on url level.")),
                ("url_issues_high", models.IntegerField(default=0, help_text="Number of high issues on url level.")),
                (
                    "url_issues_medium",
                    models.IntegerField(default=0, help_text="Number of medium issues on url level."),
                ),
                ("url_issues_low", models.IntegerField(default=0, help_text="Number of low issues on url level.")),
                (
                    "total_endpoint_issues",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "endpoint_issues_high",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "endpoint_issues_medium",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "endpoint_issues_low",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_total_issues",
                    models.IntegerField(default=0, help_text="The summed number of all vulnerabilities and failures."),
                ),
                (
                    "explained_high",
                    models.IntegerField(default=0, help_text="The number of high risk vulnerabilities and failures."),
                ),
                (
                    "explained_medium",
                    models.IntegerField(default=0, help_text="The number of medium risk vulnerabilities and failures."),
                ),
                (
                    "explained_low",
                    models.IntegerField(default=0, help_text="The number of low risk vulnerabilities and failures."),
                ),
                (
                    "explained_total_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints for this url."),
                ),
                (
                    "explained_high_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) high risk issues."),
                ),
                (
                    "explained_medium_endpoints",
                    models.IntegerField(
                        default=0, help_text="Amount of endpoints with (1 or more) medium risk issues."
                    ),
                ),
                (
                    "explained_low_endpoints",
                    models.IntegerField(default=0, help_text="Amount of endpoints with (1 or more) low risk issues."),
                ),
                (
                    "explained_total_url_issues",
                    models.IntegerField(default=0, help_text="Total amount of issues on url level."),
                ),
                (
                    "explained_url_issues_high",
                    models.IntegerField(default=0, help_text="Number of high issues on url level."),
                ),
                (
                    "explained_url_issues_medium",
                    models.IntegerField(default=0, help_text="Number of medium issues on url level."),
                ),
                (
                    "explained_url_issues_low",
                    models.IntegerField(default=0, help_text="Number of low issues on url level."),
                ),
                (
                    "explained_total_endpoint_issues",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_endpoint_issues_high",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_endpoint_issues_medium",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                (
                    "explained_endpoint_issues_low",
                    models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
                ),
                ("when", models.DateTimeField(db_index=True)),
                (
                    "calculation",
                    jsonfield.fields.JSONField(
                        help_text="Contains JSON with a calculation of all scanners at this moment. The rating can be spread out over multiple endpoints, which might look a bit confusing. Yet it is perfectly possible as some urls change their IP every five minutes and scans are spread out over days."
                    ),
                ),
                ("url", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.Url")),
            ],
            options={
                "verbose_name": "Url Rating",
                "verbose_name_plural": "Url Ratings",
                "db_table": "map_urlreport",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="VulnerabilityStatistic",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "country",
                    django_countries.fields.CountryField(
                        db_index=True, help_text="Part of the combination shown on the map.", max_length=2
                    ),
                ),
                ("when", models.DateField()),
                ("scan_type", models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ("high", models.PositiveIntegerField(default=0)),
                ("medium", models.PositiveIntegerField(default=0)),
                ("low", models.PositiveIntegerField(default=0)),
                (
                    "urls",
                    models.PositiveIntegerField(
                        default=0, help_text="Makes only sense on the total number of vulnerabilities"
                    ),
                ),
                (
                    "endpoints",
                    models.PositiveIntegerField(
                        default=0, help_text="Makes only sense on the total number of vulnerabilities"
                    ),
                ),
                (
                    "organization_type",
                    models.ForeignKey(
                        help_text="Part of the combination shown on the map.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizations.OrganizationType",
                    ),
                ),
            ],
            options={
                "db_table": "map_vulnerabilitystatistic",
                "managed": True,
            },
        ),
        migrations.AlterIndexTogether(
            name="organizationreport",
            index_together={("when", "id")},
        ),
    ]

    operations = [migrations.SeparateDatabaseAndState(state_operations=state_operations)]
