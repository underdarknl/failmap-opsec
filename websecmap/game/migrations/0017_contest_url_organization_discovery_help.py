# Generated by Django 2.1.3 on 2018-12-03 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0016_auto_20181203_1053"),
    ]

    operations = [
        migrations.AddField(
            model_name="contest",
            name="url_organization_discovery_help",
            field=models.TextField(
                default="",
                help_text="HTML: information where contestants can find good sources of urls / organizations. Displayed on both the URL and Organization adding forms.",
                max_length=1024,
            ),
        ),
    ]
