# Generated by Django 2.1.5 on 2019-01-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0038_auto_20190128_1205"),
    ]

    operations = [
        migrations.AlterField(
            model_name="administrativeregion",
            name="import_message",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Information returned from the import features.",
                max_length=255,
                null=True,
            ),
        ),
    ]
