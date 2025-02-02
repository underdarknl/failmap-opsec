# Generated by Django 2.1.3 on 2018-12-11 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0042_auto_20181210_1318"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dataset",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source", models.URLField()),
                ("is_imported", models.BooleanField(default=False)),
                ("imported_on", models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
