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

menu_max_depth = 8 # maximum depth we will go on the menu no matter how far down the rabbit hole goes

# Used by menu2html() - specialized HTML code for whatever system we are integrating with 
header_html_start = ''
header_html_end = ''
group_html_start = '<li data-username="@@name@@" class="nav-item pcoded-hasmenu"> <a href="javascript:" class="nav-link">@@indent@@<span class="pcoded-micon"><i class="feather icon-folder"></i></span><span class="pcoded-mtext">@@name@@</span></a>'
group_html_end = '</ul></li>'
menu_html_start = '<li data-username=@@name@@ class="nav-item"> <a href="@@url@@" class="nav-link">@@indent@@<span class="pcoded-micon"><i class="feather icon-file-text"></i></span><span class="pcoded-mtext">@@name@@</span></a></li>'
menu_html_end = ''


#----------------------------------------------
# build the menu structure as html output  
#----------------------------------------------
@register.simple_tag(name='menu2html', takes_context=True)
def menu2html(context, menu_dict, menu_layout = {}, parent = None, depth = 0):

    html_code = ""
    request = context['request']
    my_group = request.user.groups.values_list('id', flat=True)
    if (depth > menu_max_depth):
        return(mark_safe(html_code))
    for item in menu_dict:

      if (item['group'] is None) or (item['group'] in my_group):
         if (item['menu_parent'] is None):
           if (item['menu_type'] == 3) and (item['menu_parent'] is None) and (parent is None):
              #menu/group header  
              indent = ""
              for i in range(0,depth):
                  indent = indent + "&nbsp;&nbsp;"
              output_line = group_html_start.replace('@@name@@',item['menu_name'])
              output_line = output_line.replace('@@url@@',item['menu_url'])
              output_line = output_line.replace('@@indent@@',indent)
              html_code = html_code + output_line
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                html_code = html_code + '<ul class="pcoded-submenu">'
                html_code = html_code + menu2html(context, menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
              html_code = html_code + group_html_end
           elif (item['menu_type'] == 1) and (item['menu_parent'] is None) and (parent is None):
              indent = ""
              for i in range(0,depth):
                  indent = indent + "&nbsp;&nbsp;"
              output_line = menu_html_start.replace('@@name@@',item['menu_name'])
              output_line = output_line.replace('@@url@@',item['menu_url'])
              output_line = output_line.replace('@@indent@@',indent)
              html_code = html_code + output_line
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                html_code = html_code + menu2html(context, menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
              html_code = html_code + menu_html_end
         elif (item['menu_parent'] == parent):
           if (item['menu_type'] == 3):
              indent = ""
              for i in range(0,depth):
                  indent = indent + "&nbsp;&nbsp;"
              output_line = group_html_start.replace('@@name@@',item['menu_name'])
              output_line = output_line.replace('@@url@@',item['menu_url'])
              output_line = output_line.replace('@@indent@@',indent)
              html_code = html_code + output_line
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                html_code = html_code + '<ul class="pcoded-submenu">'
                html_code = html_code + menu2html(context, menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
              html_code = html_code + group_html_end
           elif (item['menu_type'] == 1):
              indent = ""
              for i in range(0,depth):
                  indent = indent + "&nbsp;&nbsp;"
              output_line = menu_html_start.replace('@@name@@',item['menu_name'])
              output_line = output_line.replace('@@url@@',item['menu_url'])
              output_line = output_line.replace('@@indent@@',indent)
              html_code = html_code + output_line
              menu_layout[item['menu_name']] = {}
              menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type'],'id': item['id'],'parent': item['menu_parent']}
              menu_layout[item['menu_name']]['children'] = {}
              if (parent != item['id']):
                html_code = html_code + menu2html(context, menu_dict,menu_layout[item['menu_name']]['children'],item['id'],depth+1)
              html_code = html_code + menu_html_end
    return(mark_safe(html_code))
