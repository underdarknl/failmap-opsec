# Generated by Django 2.0.7 on 2018-08-14 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0041_tlsscan"),
    ]

    operations = [
        migrations.AlterField(
            model_name="endpointgenericscan",
            name="domain",
            field=models.CharField(
                blank=True, help_text="Deprecated. Text value representing the url scanned.", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="endpointgenericscanscratchpad",
            name="domain",
            field=models.CharField(
                blank=True, help_text="Deprecated. Used when there is no known Endpoint.", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="screenshot",
            name="domain",
            field=models.CharField(
                blank=True, help_text="Deprecated. Used when there is no known URL.", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="urlgenericscan",
            name="domain",
            field=models.CharField(
                blank=True, help_text="Deprecated. Text value representing the url scanned.", max_length=255, null=True
            ),
        ),
    ]
