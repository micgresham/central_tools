# Generated by Django 3.2.6 on 2022-03-16 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CentralSites',
            fields=[
                ('key', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('site_id', models.CharField(max_length=25)),
                ('address', models.CharField(max_length=200)),
                ('associated_device_count', models.CharField(blank=True, default='0', max_length=25)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('latitude', models.CharField(default='0', max_length=50, null=True)),
                ('longitude', models.CharField(default='0', max_length=50, null=True)),
                ('site_details', jsonfield.fields.JSONField(default=dict)),
                ('site_name', models.CharField(max_length=101)),
                ('state', models.CharField(max_length=100)),
                ('tags', models.CharField(blank=True, max_length=100, null=True)),
                ('zipcode', models.CharField(default='00000', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='user-1.png', upload_to='profile_images')),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('central_url', models.URLField(default='')),
                ('central_custID', models.CharField(default='', max_length=100)),
                ('central_clientID', models.CharField(default='', max_length=100)),
                ('central_client_secret', models.CharField(default='', max_length=100)),
                ('central_token', models.CharField(default='', max_length=100)),
                ('central_refresh_token', models.CharField(default='', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
