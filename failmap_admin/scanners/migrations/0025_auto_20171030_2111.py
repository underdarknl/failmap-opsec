# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanners', '0024_auto_20171030_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlip',
            name='discovered_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
