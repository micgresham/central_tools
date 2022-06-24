# -*- encoding: utf-8 -*-
"""
"""

#--------------------------------------------------------------------
# Code incorporated from https://github.com/luminousmen/django-sql
# Copyright (C) 2016, Kirill Bobrov
#--------------------------------------------------------------------

from django import template
from datetime import datetime
from django.conf import settings
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views import View
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from pprint import pprint

import requests
import json
import urllib.parse
import time
import math


#--------------------------------------------------
#common API functions from common_views 
#--------------------------------------------------
#from apps.home.common_views import get_site_inventory
#from apps.home.common_views import test_central
#from apps.home.common_views import update_sites
#from apps.home.common_views import update_tvariable
#from apps.home.common_views import update_tmdvariable
#from apps.home.common_views import get_variables
#from apps.home.common_views import get_stack_conductor
#from apps.home.common_views import set_variable
#from apps.home.common_views import get_autocommit
#from apps.home.common_views import set_autocommit

#-----------------------------------------
#Forms for the workflow
#-----------------------------------------

from django.db import models, connection
from django.forms import ModelForm, Textarea
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.template.defaulttags import register # needed for dynamic menus
from .pymenu import Menu

from django.utils.safestring import mark_safe
#-----------------------------------------
#Views for the workflow
#-----------------------------------------

def test_menu(request):

    context = {}

    context['title'] = "test_menu"
    menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
    context['menu'] = menu

    return render(request, 'home/WFtest.html', context)


def format_sql(query):
    keywords = ['select', 'from', 'as', 'join', 'left', 'on',
                'where', 'and', 'case', 'else', 'end', 'is',
                'null', 'union', 'order', 'by', 'concat',
                'to_char', 'limit', 'or']
    new_query = []
    flag = False

    for word in query.split():
        if word in keywords:
            word = word.upper()

        word += ' '
        if '(' in word and ')' not in word:
            flag = True
            new_query.append(word)
            continue
        if flag and (')' not in word or '(' in word):
            new_query.append(word)
            continue
        else:
            flag = False

        if word.strip().endswith(','):
            word += '\n\t'
        if word.strip() == 'FROM':
            word = '\n' + word
        if word.strip() == 'WHERE':
            word = '\n' + word + '\n\t'
        if word.strip() in ('LEFT', 'AND'):
            word = '\n\t' + word
        if word.strip() == 'SELECT':
            word += '\n\t'
        if word.strip() in ('WHEN', 'ELSE', 'END'):
            word = '\n\t\t' + word

        new_query.append(word)

    return ''.join(new_query)

