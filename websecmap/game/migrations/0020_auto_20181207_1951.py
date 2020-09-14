# Generated by Django 2.1.3 on 2018-12-07 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0019_auto_20181207_1142"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationsubmission",
            name="organization_name",
            field=models.CharField(
                default="unknown", help_text="The contest the team is participating in.", max_length=250
            ),
        ),
    ]
