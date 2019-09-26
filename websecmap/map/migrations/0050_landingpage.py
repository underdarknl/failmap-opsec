# Generated by Django 2.2.1 on 2019-09-26 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0049_auto_20190604_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory', models.CharField(blank=True, db_index=True, help_text='A directory to this landing page. For example: municipality/ or gemeente/ or preview/ etc. This directory will be added to your map urls. Do not use things like /admin/, as that will conflict with existing urls and your application might not boot without manual database edits. Do not use a beginning slash.', max_length=255, null=True)),
                ('enabled', models.BooleanField(default=False,
                                                help_text='If this directory is enabled. You may need to restart the application when changing this.')),
                ('map_configuration', models.ForeignKey(help_text='To what map configuration this landing page is relevant.',
                                                        on_delete=django.db.models.deletion.CASCADE, to='map.Configuration')),
            ],
        ),
    ]
