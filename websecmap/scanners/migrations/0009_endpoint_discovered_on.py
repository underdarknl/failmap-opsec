# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0008_auto_20170908_1218"),
    ]

    operations = [
        migrations.AddField(
            model_name="endpoint",
            name="discovered_on",
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
