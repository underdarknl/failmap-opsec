# Generated by Django 2.0.4 on 2018-04-10 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0005_auto_20180409_2156"),
    ]

    operations = [
        migrations.RenameField(
            model_name="organizationsubmission",
            old_name="organisation_in_system",
            new_name="organization_in_system",
        ),
    ]
