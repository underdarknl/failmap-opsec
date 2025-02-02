# Generated by Django 2.2.10 on 2020-05-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0070_internetnlv2scan_internetnlv2statelog"),
    ]

    operations = [
        migrations.AddField(
            model_name="internetnlv2scan",
            name="last_state_change",
            field=models.DateTimeField(
                blank=True,
                help_text="When this state changed the last time, so no in-between updates about the state.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="internetnlv2statelog",
            name="last_state_check",
            field=models.DateTimeField(
                blank=True,
                help_text="Last time this state was written to this field, which can happen regularly.",
                null=True,
            ),
        ),
    ]
