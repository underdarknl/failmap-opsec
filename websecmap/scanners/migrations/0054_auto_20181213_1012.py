# Generated by Django 2.1.3 on 2018-12-13 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0053_auto_20181122_1514"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="endpointgenericscan",
            name="domain",
        ),
        migrations.RemoveField(
            model_name="screenshot",
            name="domain",
        ),
        migrations.RemoveField(
            model_name="urlgenericscan",
            name="domain",
        ),
    ]
