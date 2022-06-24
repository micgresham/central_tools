# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Profile
from .pymenu import Menu

# Register your models here.

admin.site.register(Menu)
admin.site.register(Profile)
