# Generated by Django 2.0.4 on 2018-04-19 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0013_administrativeregion_imported"),
    ]

    operations = [
        migrations.AddField(
            model_name="administrativeregion",
            name="resampling_resolution",
            field=models.FloatField(
                default="0.001",
                help_text="This is used in the algorithm that reduces datapoints in map shapes: this saves a lot of data. value here should make the map look decent when the entire country is visible but may be somewhat blocky when zooming in. The smaller the number, the more detail.",
            ),
        ),
    ]
