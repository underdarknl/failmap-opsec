# Generated by Django 2.0.7 on 2018-08-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0019_auto_20180824_1442"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizationrating",
            name="endpoint_issues_high",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="endpoint_issues_low",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="endpoint_issues_medium",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="total_endpoint_issues",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="total_url_issues",
            field=models.IntegerField(default=0, help_text="Total amount of issues on url level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="url_issues_high",
            field=models.IntegerField(default=0, help_text="Number of high issues on url level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="url_issues_low",
            field=models.IntegerField(default=0, help_text="Number of low issues on url level."),
        ),
        migrations.AddField(
            model_name="organizationrating",
            name="url_issues_medium",
            field=models.IntegerField(default=0, help_text="Number of medium issues on url level."),
        ),
    ]
