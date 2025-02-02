# Generated by Django 2.1.7 on 2019-03-08 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0004_auto_20190222_1421"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizationreport",
            name="endpoint_ok",
            field=models.IntegerField(default=0, help_text="Zero issues on these endpoints."),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="ok",
            field=models.IntegerField(default=0, help_text="No issues found at all."),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="ok_endpoints",
            field=models.IntegerField(default=0, help_text="Amount of endpoints with zero issues."),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="ok_urls",
            field=models.IntegerField(default=0, help_text="Amount of urls with zero issues."),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="url_ok",
            field=models.IntegerField(default=0, help_text="Zero issues on these urls."),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="endpoint_ok",
            field=models.IntegerField(default=0, help_text="Zero issues."),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="ok",
            field=models.IntegerField(default=0, help_text="Url with zero issues."),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="ok_endpoints",
            field=models.IntegerField(default=0, help_text="Endpoints with zero issues."),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="url_ok",
            field=models.IntegerField(default=0, help_text="Zero issues."),
        ),
    ]
