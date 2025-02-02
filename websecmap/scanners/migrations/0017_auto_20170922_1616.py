# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0016_auto_20170922_1612"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endpointgenericscan",
            name="type",
            field=models.CharField(
                db_index=True,
                help_text="The type of scan that was performed. Instead of having different tables for eachscan, this label separates the scans.",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="endpointgenericscanscratchpad",
            name="type",
            field=models.CharField(
                db_index=True,
                help_text="The type of scan that was performed. Instead of having different tables for eachscan, this label separates the scans.",
                max_length=60,
            ),
        ),
    ]
