# Generated by Django 2.1.3 on 2018-12-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pro", "0008_subdomaindatafeed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="urllist",
            name="urls",
            field=models.ManyToManyField(blank=True, to="organizations.Url"),
        ),
    ]
