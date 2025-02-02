# Generated by Django 2.2.1 on 2019-06-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0048_auto_20190412_1132"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizationreport",
            name="endpoint_not_applicable",
            field=models.IntegerField(
                default=0, help_text="Amount of things that are not applicable on this endpoint."
            ),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="endpoint_not_testable",
            field=models.IntegerField(
                default=0, help_text="Amount of things that could not be tested on this endpoint."
            ),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="not_applicable",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="not_testable",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="url_not_applicable",
            field=models.IntegerField(default=0, help_text="Amount of things that are not applicable on this url."),
        ),
        migrations.AddField(
            model_name="organizationreport",
            name="url_not_testable",
            field=models.IntegerField(default=0, help_text="Amount of things that could not be tested on this url."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="endpoint_issues_high",
            field=models.IntegerField(default=0, help_text="Total amount of high risk issues on this endpoint."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="endpoint_issues_low",
            field=models.IntegerField(default=0, help_text="Total amount of low risk issues on this endpoint"),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="endpoint_issues_medium",
            field=models.IntegerField(default=0, help_text="Total amount of medium risk issues on this endpoint."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="endpoint_ok",
            field=models.IntegerField(
                default=0, help_text="Amount of measurements that resulted in an OK score on this endpoint."
            ),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="explained_total_url_issues",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="explained_url_issues_high",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="explained_url_issues_low",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="explained_url_issues_medium",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="high",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="low",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="medium",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="ok",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="total_endpoint_issues",
            field=models.IntegerField(
                default=0,
                help_text="A sum of all endpoint issues for this endpoint, it includes all high, medium and lows.",
            ),
        ),
        migrations.AlterField(
            model_name="organizationreport",
            name="total_issues",
            field=models.IntegerField(default=0),
        ),
    ]
