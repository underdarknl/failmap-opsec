# Generated by Django 2.1.3 on 2018-12-20 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pro", "0009_auto_20181220_1709"),
    ]

    operations = [
        migrations.AddField(
            model_name="subdomaindatafeed",
            name="domain",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="subdomaindatafeed",
            name="topleveldomain",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
