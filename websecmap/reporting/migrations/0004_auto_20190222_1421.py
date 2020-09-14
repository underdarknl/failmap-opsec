# Generated by Django 2.1.7 on 2019-02-22 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0003_auto_20190222_1128"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="organizationreport",
            options={
                "get_latest_by": "when",
                "verbose_name": "Organization Report",
                "verbose_name_plural": "Organization Reports",
            },
        ),
        migrations.AlterModelOptions(
            name="urlreport",
            options={"managed": True, "verbose_name": "Url Report", "verbose_name_plural": "Url Reports"},
        ),
    ]
