# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 16:17
from __future__ import unicode_literals

from django.db import migrations, models
from datetime import date, datetime, timedelta


class Migration(migrations.Migration):

    dependencies = [
        ('scanners', '0002_auto_20170226_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='tlsqualysscan',
            name='rating_determined_on',
            field=models.DateTimeField(auto_now_add=True, default="2017-01-01"),
            preserve_default=False,
        ),
    ]
