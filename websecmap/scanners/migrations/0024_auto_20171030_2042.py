# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 20:42
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0018_auto_20171017_1317"),
        ("scanners", "0023_endpointip_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="UrlIp",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "ip",
                    models.CharField(
                        help_text="IPv4 or IPv6 Address. Addresses have to be normalized to the compressed representation: removing as many zeros as possible. For example:  IPv6: abcd:0000:0000:00fd becomes abcd::fd, or IPv4: 127.000.000.001 = 127.0.0.1",
                        max_length=255,
                    ),
                ),
                (
                    "rdns_name",
                    models.CharField(
                        help_text="The reverse name can be a server name, containing a provider or anything else.It might contain the name of a yet undiscovered url or hint to a service.",
                        max_length=255,
                    ),
                ),
                ("discovered_on", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "is_unused",
                    models.IntegerField(
                        default=False,
                        help_text="If the address was used in the past, but not anymore.It's possible that the same address is more than once associated with and endpoint over time, as some providersrotate a set of IP addresses.",
                    ),
                ),
                ("is_unused_since", models.DateTimeField(blank=True, null=True)),
                ("is_unused_reason", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "url",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="organizations.Url"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="endpointip",
            name="endpoint",
        ),
        migrations.RemoveField(
            model_name="endpointip",
            name="url",
        ),
        migrations.DeleteModel(
            name="EndpointIp",
        ),
    ]
