# Generated by Django 2.1.5 on 2019-01-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0033_auto_20190123_1613"),
    ]

    operations = [
        migrations.AlterField(
            model_name="administrativeregion",
            name="import_message",
            field=models.CharField(
                default="", help_text="Information returned from the import features.", max_length=255
            ),
        ),
    ]
