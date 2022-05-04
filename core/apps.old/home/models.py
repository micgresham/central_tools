# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
import os.path
import jsonfield

# Create your models here.

class Profile(models.Model):
         user = models.OneToOneField(User, on_delete=models.CASCADE)
         avatar = models.ImageField(default='user-1.png', upload_to='profile_images')
         image = models.ImageField(upload_to='profile_image' , blank=True)
         central_url = models.URLField(default='')
#         central_username = models.CharField(max_length=100, default='')
#         central_password = models.CharField(max_length=100, default='')
         central_custID = models.CharField(max_length=100, default='')
         central_clientID = models.CharField(max_length=100, default='')
         central_client_secret = models.CharField(max_length=100, default='')
         central_token = models.CharField(max_length=100, default='')
         central_refresh_token = models.CharField(max_length=100, default='')
         central_tokenID = models.CharField(max_length=100, default='')
         

         def __str__(self):
                          return self.user.username
         
             # resizing images

         def save(self, *args, **kwargs):
             super().save()

             if os.path.isfile(self.avatar.path):
                img = Image.open(self.avatar.path)
             else:
                img = Image.open(settings.MEDIA_ROOT + '/user-1.png')

             if img.height > 150 or img.width > 150:
                new_img = (150, 150)
                img.thumbnail(new_img)
                img.save(self.avatar.path)

#class CentralSites(models.Model):
#
#    key=models.CharField(primary_key=True, max_length=200)
#    username=models.CharField(max_length=200)
#    site_id=models.CharField(max_length=25)
#    address=models.CharField(max_length=200)
#    associated_device_count=models.CharField(max_length=25,blank=True, default="0")
#    city=models.CharField(max_length=100)
#    country=models.CharField(max_length=100)
#    latitude=models.CharField(max_length=50, null=True, default="0")
#    longitude=models.CharField(max_length=50, null=True, default="0")
#    site_details=jsonfield.JSONField()
#    site_name=models.CharField(max_length=101)
#    state=models.CharField(max_length=100)
#    tags=models.CharField(max_length=100, blank=True, null=True)
#    zipcode=models.CharField(max_length=50, default="00000")

class CentralSites(models.Model):
    customer_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    site_id = models.CharField(max_length=25)
    site_name = models.CharField(primary_key=True, max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    associated_device_count = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True, default="0")
    longitude = models.CharField(max_length=20, blank=True, null=True, default="0")
    name = models.CharField(max_length=20, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    last_refreshed = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sites'
        unique_together = (('customer_id', 'site_id'),)


