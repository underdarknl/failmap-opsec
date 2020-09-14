# Generated by Django 2.0.3 on 2018-03-21 10:00

import jsonfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0027_auto_20180321_0939"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coordinate",
            name="edit_area",
            field=jsonfield.fields.JSONField(
                blank=True,
                help_text="The results of this field are saved in the area and geojsontype. It's possible to edit the area field directly, which overwrites this field. Changing both the manual option takes preference.",
                max_length=10000,
                null=True,
            ),
        ),
    ]
