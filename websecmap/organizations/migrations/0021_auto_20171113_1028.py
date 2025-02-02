# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 10:28
from __future__ import unicode_literals

from django.db import migrations, models

import websecmap.organizations.models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0020_auto_20171112_1149"),
    ]

    operations = [
        migrations.AlterField(
            model_name="promise",
            name="created_on",
            field=models.DateTimeField(blank=True, default=websecmap.organizations.models.today, null=True),
        ),
        migrations.AlterField(
            model_name="promise",
            name="expires_on",
            field=models.DateTimeField(
                blank=True,
                default=websecmap.organizations.models.seven_days_in_the_future,
                help_text="When in the future this promise is expected to be fulfilled.",
                null=True,
            ),
        ),
    ]
