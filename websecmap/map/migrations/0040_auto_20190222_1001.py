# Generated by Django 2.1.7 on 2019-02-22 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0053_url_do_not_find_subdomains'),
        ('map', '0039_auto_20190129_0955'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrganizationRating',
            new_name='OrganizationReport',
        ),
        migrations.RenameModel(
            old_name='UrlRating',
            new_name='UrlReport',
        ),
    ]
