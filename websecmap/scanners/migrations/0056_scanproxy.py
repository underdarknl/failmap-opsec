# Generated by Django 2.1.5 on 2019-01-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scanners", "0055_auto_20181213_1218"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScanProxy",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "address",
                    models.CharField(
                        help_text="An internet address, including the http/https scheme. Works only on IP. Username / pass can beadded in the address. For example: https://username:password@192.168.1.1:1337/",
                        max_length=255,
                    ),
                ),
                (
                    "currently_used_in_tls_qualys_scan",
                    models.BooleanField(
                        default=False,
                        help_text="Set's the proxy as in use, so that another scanner knows that this proxy is being used at this moment. After a scan is completed, the flag has to be disabled. This of course goes wrong with crashes. So once in a while, if things fail or whatever, this might have to be resetted.",
                    ),
                ),
                (
                    "is_dead",
                    models.BooleanField(
                        default=False,
                        help_text="Use the 'declare dead' button to autofill the date. If the port is closed, or the endpoint is otherwisenot reachable over the specified protocol, then markit as dead. A scanner for this port/protocol can alsodeclare it dead. This port is closed on this protocol.",
                    ),
                ),
                ("is_dead_since", models.DateTimeField(blank=True, null=True)),
                ("is_dead_reason", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "out_of_resource_counter",
                    models.IntegerField(
                        default=0,
                        help_text="Every time the proxy has not enough resources, this number will increase with one. A too high number makes it easy not to use this proxy anymore.",
                    ),
                ),
            ],
        ),
    ]
