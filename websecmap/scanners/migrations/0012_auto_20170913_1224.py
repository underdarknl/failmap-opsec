# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0011_screenshot"),
    ]

    operations = [
        migrations.AddField(
            model_name="tlsqualysscan",
            name="qualys_message",
            field=models.CharField(
                blank=True, help_text="Whatever Qualys said about the endpoint", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="endpoint",
            name="is_dead",
            field=models.IntegerField(
                default=False,
                help_text="If the port is closed, or the endpoint is otherwisenot reachable over the specified protocol, then markit as dead. A scanner for this port/protocol can alsodeclare it dead. This port is closed on this protocol.",
            ),
        ),
    ]
