# Generated by Django 2.2.10 on 2020-08-24 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0077_auto_20200820_1254"),
    ]

    operations = [
        migrations.AddField(
            model_name="plannedscan",
            name="requested_at_when_date",
            field=models.DateField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="plannedscan",
            name="requested_at_when",
            field=models.DateTimeField(),
        ),
    ]
