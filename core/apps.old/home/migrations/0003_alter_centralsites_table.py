# Generated by Django 3.2.6 on 2022-04-05 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_centralsites_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='centralsites',
            table='sites',
        ),
    ]
