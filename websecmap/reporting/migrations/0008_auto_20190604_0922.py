# Generated by Django 2.2.1 on 2019-06-04 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reporting", "0007_auto_20190412_1132"),
    ]

    operations = [
        migrations.AddField(
            model_name="urlreport",
            name="endpoint_not_applicable",
            field=models.IntegerField(
                default=0, help_text="Amount of things that are not applicable on this endpoint."
            ),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="endpoint_not_testable",
            field=models.IntegerField(
                default=0, help_text="Amount of things that could not be tested on this endpoint."
            ),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="not_applicable",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="not_testable",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="url_not_applicable",
            field=models.IntegerField(default=0, help_text="Amount of things that are not applicable on this url."),
        ),
        migrations.AddField(
            model_name="urlreport",
            name="url_not_testable",
            field=models.IntegerField(default=0, help_text="Amount of things that could not be tested on this url."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="endpoint_issues_high",
            field=models.IntegerField(default=0, help_text="Total amount of high risk issues on this endpoint."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="endpoint_issues_low",
            field=models.IntegerField(default=0, help_text="Total amount of low risk issues on this endpoint"),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="endpoint_issues_medium",
            field=models.IntegerField(default=0, help_text="Total amount of medium risk issues on this endpoint."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="endpoint_ok",
            field=models.IntegerField(
                default=0, help_text="Amount of measurements that resulted in an OK score on this endpoint."
            ),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="explained_total_url_issues",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="explained_url_issues_high",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="explained_url_issues_low",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="explained_url_issues_medium",
            field=models.IntegerField(default=0, help_text="Total amount of issues on endpoint level."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="high",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="low",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="medium",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="ok",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="ok_endpoints",
            field=models.IntegerField(default=0, help_text="Amount of endpoints with zero issues."),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="total_endpoint_issues",
            field=models.IntegerField(
                default=0,
                help_text="A sum of all endpoint issues for this endpoint, it includes all high, medium and lows.",
            ),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="total_issues",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="urlreport",
            name="url_ok",
            field=models.IntegerField(default=0, help_text="Zero issues on these urls."),
        ),
    ]
