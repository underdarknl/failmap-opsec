# Generated by Django 2.2.10 on 2020-08-20 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0076_auto_20200816_0944"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plannedscan",
            name="requested_at_when",
            field=models.DateTimeField(db_index=True),
        ),
    ]
