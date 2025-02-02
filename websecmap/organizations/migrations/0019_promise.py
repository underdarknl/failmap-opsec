# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-11 09:52
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0018_auto_20171017_1317"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promise",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notes", models.TextField(help_text="Context information about the promise (eg: ticket reference).")),
                ("created_on", models.DateTimeField(auto_now_add=True, null=True)),
                ("expires_on", models.DateTimeField(blank=True, null=True)),
                (
                    "organization",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="organizations.Organization"),
                ),
            ],
        ),
    ]
