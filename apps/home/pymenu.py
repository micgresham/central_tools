# -*- encoding: utf-8 -*-
"""
pymenu - Dynamic html menu system in python3
Copyright (c) 2022 - Michael Gresham - mgresham@e-secondstar.com
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
from PIL import Image
import os.path
import jsonfield
import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.template.defaulttags import register # needed for dynamic menus
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

#---------------------------------------------------------------
# model(s)
#---------------------------------------------------------------

class Menu(models.Model):
        MENU_TYPES = (
         (1, 'Menu Item'),
         (3, 'Menu Group'),
        )

        id = models.AutoField(primary_key=True)
        menu_name = models.CharField(max_length = 50)
        menu_url = models.CharField(max_length = 300,default="/")
        group = models.ForeignKey(Group, blank=True,null=True,on_delete=models.CASCADE)
        menu_type = models.IntegerField(choices=MENU_TYPES)
#        menu_parent = models.ManyToManyField('self',blank=True,null=True)
        menu_parent = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)

        class Meta:
          db_table = 'menus'

        def __str__(self):
          return self.menu_name

        def save(self, *args, **kwargs):
          super().save()

        menu_objects =models.Manager()

#---------------------------------------------------------------
# views
#---------------------------------------------------------------

my_group = {1,2,3}
menu_max_depth = 8 # maximum depth we will go on the menu no matter how far down the rabbit hole goes

# Used by menu2html() - specialized HTML code for whatever system we are integrating with 
header_html_start = ''
header_html_end = ''
group_html_start = '<li data-username="@@name@@" class="nav-item pcoded-hasmenu"> <a href="javascript:" class="nav-link">@@indent@@<span class="pcoded-micon"><i class="feather icon-folder"></i></span><span class="pcoded-mtext">@@name@@</span></a>'
group_html_end = '</ul></li>'
menu_html_start = '<li data-username=@@name@@ class="nav-item"> <a href="@@url@@" class="nav-link">@@indent@@<span class="pcoded-micon"><i class="feather icon-file-text"></i></span><span class="pcoded-mtext">@@name@@</span></a></li>'
menu_html_end = ''

#----------------------------------------------
# build the menu structure as a dictionary
#----------------------------------------------
def menu2dict(menu_dict, menu_layout = {}, parent = None, depth = 0):
    if (depth > menu_max_depth):
        print("***MAX DEPTH***")
        return(menu_layout)
    for item in menu_dict:
      if (item['group'] is None) or (item['group'] in my_group):
         if (item['menu_parent'] is None):
           if (item['menu_type'] == 3) and (item['menu_parent'] is None) and (parent is None):
              for i in range(0,depth):
                  print("--",end = '')
              print(item['menu_name']," (GROUP)")
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                menu_layout[item['menu_name']]['children'] = menu2dict(menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
           elif (item['menu_type'] == 1) and (item['menu_parent'] is None) and (parent is None):
              for i in range(0,depth):
                  print("--",end = '')
              print(item['menu_name'])
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                menu_layout[item['menu_name']]['children'] = menu2dict(menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
         elif (item['menu_parent'] == parent):
           if (item['menu_type'] == 3):
              for i in range(0,depth):
                  print("--",end = '')
              print(item['menu_name']," (GROUP)")
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                menu_layout[item['menu_name']]['children'] = menu2dict(menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
           elif (item['menu_type'] == 1):
              for i in range(0,depth):
                  print("--",end = '')
              print(item['menu_name'])
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                menu_layout[item['menu_name']]['children'] = menu2dict(menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
    return(menu_layout)

def make_menu(request):

        context = {}

        context['title'] = "test_menu"
        my_group = request.user.groups.values_list('id', flat=True)
        menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
        menu_layout = {}
        menu_layout = menu2dict(menu)
        return menu_layout


