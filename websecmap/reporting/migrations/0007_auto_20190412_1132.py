# Generated by Django 2.2 on 2019-04-12 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0006_auto_20190401_1356"),
    ]

    operations = [
        migrations.RenameField(
            model_name="urlreport",
            old_name="when",
            new_name="at_when",
        ),
    ]
