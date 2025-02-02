# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 17:23
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0017_auto_20170922_1616"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endpointgenericscan",
            name="endpoint",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="scanners.Endpoint"
            ),
        ),
        migrations.AlterField(
            model_name="endpointgenericscan",
            name="rating_determined_on",
            field=models.DateTimeField(
                help_text="This is when the current rating was first discovered. It may be obsoleted byanother rating or explanation (which might have the same rating). This date cannot change once it's set."
            ),
        ),
        migrations.AlterField(
            model_name="screenshot",
            name="endpoint",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="scanners.Endpoint"
            ),
        ),
    ]
