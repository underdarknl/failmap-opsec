# Generated by Django 2.1.5 on 2019-01-23 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0032_auto_20181218_0915"),
    ]

    operations = [
        migrations.AddField(
            model_name="administrativeregion",
            name="import_message",
            field=models.CharField(
                blank=True, help_text="Information returned from the import features.", max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="administrativeregion",
            name="organization_type",
            field=models.ForeignKey(
                help_text="The organization type desired to import. Not all organization types might be present in this list by default. Create new ones accordingly.",
                on_delete=django.db.models.deletion.CASCADE,
                to="organizations.OrganizationType",
            ),
        ),
    ]
