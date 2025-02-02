# Generated by Django 2.0.7 on 2018-08-23 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0036_url_onboarding_stage_set_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="url",
            name="computed_domain",
            field=models.CharField(
                blank=True,
                help_text="Automatically computed by tldextract on save. Data entered manually will be overwritten.",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="url",
            name="computed_subdomain",
            field=models.CharField(
                blank=True,
                help_text="Automatically computed by tldextract on save. Data entered manually will be overwritten.",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="url",
            name="computed_suffix",
            field=models.CharField(
                blank=True,
                help_text="Automatically computed by tldextract on save. Data entered manually will be overwritten.",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="url",
            name="url",
            field=models.CharField(
                help_text="Lowercase url name. For example: mydomain.tld or subdomain.domain.tld", max_length=255
            ),
        ),
    ]
