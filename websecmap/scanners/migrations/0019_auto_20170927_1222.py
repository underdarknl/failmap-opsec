# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 12:22
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0018_auto_20170922_1723"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endpoint",
            name="url",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="organizations.Url"
            ),
        ),
    ]
