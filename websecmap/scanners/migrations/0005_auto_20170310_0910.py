# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0004_auto_20170227_1622"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tlsqualysscan",
            name="pending",
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name="tlsqualysscan",
            name="pending_since",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="tlsqualysscan",
            name="rating_determined_on",
            field=models.DateTimeField(),
        ),
    ]
