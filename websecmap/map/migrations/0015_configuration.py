# Generated by Django 2.0.4 on 2018-04-20 07:54

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0032_auto_20180410_0957"),
        ("map", "0014_administrativeregion_resampling_resolution"),
    ]

    operations = [
        migrations.CreateModel(
            name="Configuration",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "country",
                    django_countries.fields.CountryField(
                        db_index=True, help_text="Part of the combination shown on the map.", max_length=2
                    ),
                ),
                (
                    "is_displayed",
                    models.BooleanField(default=False, help_text="Whether this combination is shown on the map."),
                ),
                (
                    "is_displayed_as_default",
                    models.BooleanField(
                        default=False,
                        help_text="Determines if this is the default view. Only one can be selected to be displayed first. If there are multiple, the first one is used. This can lead to unexpected results.",
                    ),
                ),
                ("display_order", models.PositiveIntegerField(default=0, verbose_name="order")),
                (
                    "is_scanned",
                    models.BooleanField(
                        default=False, help_text="Whether this combination will be scanned by the scanners."
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
        ),
    ]
