# Generated by Django 2.0.8 on 2018-10-25 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0027_auto_20181025_0917"),
    ]

    operations = [
        migrations.AddField(
            model_name="mapdatacache",
            name="cached_on",
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
