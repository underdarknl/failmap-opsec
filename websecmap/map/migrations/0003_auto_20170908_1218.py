# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-08 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0002_auto_20170828_1529"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationrating",
            name="when",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="urlrating",
            name="when",
            field=models.DateTimeField(db_index=True),
        ),
    ]
