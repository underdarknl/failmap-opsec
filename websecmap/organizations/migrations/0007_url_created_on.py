# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0006_auto_20170906_0944"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="created_on",
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
