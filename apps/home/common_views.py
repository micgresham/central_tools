# -*- encoding: utf-8 -*-
"""
"""

from django import template
from datetime import datetime
from django.conf import settings
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views import View

import requests
import json
import urllib.parse
import time
from datetime import datetime, timedelta
import math

from .models import CentralSites
from .models import Menu

#------------------------------------------------------
# make_menu - Creates the structure for the dyamic 
#             menu system.  
#------------------------------------------------------

from django.contrib.admin.views.decorators import staff_member_required
from django.template.defaulttags import register # needed for dynamic menus
from django.utils.safestring import mark_safe

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

#@staff_member_required
def make_menu(request):

    context = {}

    context['title'] = "test_menu"
    my_group = request.user.groups.values_list('id', flat=True)
    menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
    menu_layout = {}
    for item in menu: #level 1
        item_group = item['group']
        item_type = item['menu_type']
        if (item_group is None) or (item_group in my_group):
            if (item['menu_type'] == 3) and (item['menu_parent'] is None):
                print(item['menu_name']," (GROUP)")
                menu_layout[item['menu_name']] = {}
                menu_layout[item['menu_name']]['name'] = item['menu_name'] 
                menu_layout[item['menu_name']]['type'] = 3 
                menu_layout[item['menu_name']]['url'] = "" 
                menu_layout[item['menu_name']]['children'] = {}
                for item2 in menu: #level 2
                    if (item2['menu_type'] == 1) and (item2['menu_parent'] == item['id'] and ((item2['group'] is None) or item2['group'] in my_group)):
                      print("------",item2['menu_name'])
                      menu_layout[item['menu_name']]['children'][item2['menu_name']] = {'name': item2['menu_name'],'url': item2['menu_url'],'type': item2['menu_type']}
                      menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'] = {}
                      for item3 in menu: #level 3
                        if (item3['menu_type'] == 1) and (item3['menu_parent'] == item2['id'] and ((item3['group'] is None) or item3['group'] in my_group)):
                           print("-----------",item3['menu_name'])
                           menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'][item3['menu_name']] = {'name': item3['menu_name'], 'url': item3['menu_url'],'type': item3['menu_type'] }
                        elif (item3['menu_type'] == 3) and (item3['menu_parent'] == item2['id'] and ((item3['group'] is None) or item3['group'] in my_group)):
                           print("-----------",item3['menu_name'],"  (GROUP)")
                           menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'][item3['menu_name']] = {'name': item3['menu_name'], 'url': item3['menu_url'],'type': item3['menu_type'] }

                    elif (item2['menu_type'] == 3) and (item2['menu_parent'] == item['id'] and ((item2['group'] is None) or item2['group'] in my_group)):
                      print("------",item2['menu_name']," (GROUP)")
                      menu_layout[item['menu_name']]['children'][item2['menu_name']] = {'name': item2['menu_name'],'url': item2['menu_url'],'type': item2['menu_type']}
                      menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'] = {}
                      for item3 in menu: #level 3
                        if (item3['menu_type'] == 1) and (item3['menu_parent'] == item2['id'] and ((item3['group'] is None) or item3['group'] in my_group)):
                           print("-----------",item3['menu_name'])
                           menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'][item3['menu_name']] = {'name': item3['menu_name'], 'url': item3['menu_url'],'type': item3['menu_type'] }


            elif (item_type == 1) and (item['menu_parent'] is None):
                print(item['menu_name'])
                menu_layout[item['menu_name']] = {}
                menu_layout[item['menu_name']] = {'name': item['menu_name'],'url': item['menu_url'],'type': item['menu_type']}
                menu_layout[item['menu_name']]['children'] = {}
                for item2 in menu:
                    if (item2['menu_type'] == 1) and (item2['menu_parent'] == item['id'] and ((item2['group'] is None) or item2['group'] in my_group)):
                      print("------",item2['menu_name'])
                      menu_layout[item['menu_name']]['children'][item2['menu_name']] = {'name': item2['menu_name'],'url': item2['menu_url'],'type': item2['menu_type']}
                      menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'] = {}
                      for item3 in menu:
                        if (item3['menu_type'] == 1) and (item3['menu_parent'] == item2['id'] and ((item3['group'] is None) or item3['group'] in my_group)):
                           print("-----------",item3['menu_name'])
                           menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'][item3['menu_name']] = {'name': item3['menu_name'], 'url': item3['menu_url'],'type': item3['menu_type'] }
                    elif (item2['menu_type'] == 3) and (item2['menu_parent'] == item['id'] and ((item2['group'] is None) or item2['group'] in my_group)):
                      print("------",item2['menu_name']," (GROUP)")
                      menu_layout[item['menu_name']]['children'][item2['menu_name']] = {'name': item2['menu_name'],'url': item2['menu_url'],'type': item2['menu_type']}
                      menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'] = {}
                      for item3 in menu: #level 3
                        if (item3['menu_type'] == 1) and (item3['menu_parent'] == item2['id'] and ((item3['group'] is None) or item3['group'] in my_group)):
                           print("-----------",item3['menu_name'])
                           menu_layout[item['menu_name']]['children'][item2['menu_name']]['children'][item3['menu_name']] = {'name': item3['menu_name'], 'url': item3['menu_url'],'type': item3['menu_type'] }



#    pprint(menu_layout)
    return menu_layout


@login_required(login_url="/login/")
def test_central(request, test=True):


    current_user = request.user.profile

    clientID = current_user.central_clientID
    custID = current_user.central_custID
    client_secret = current_user.central_client_secret
    refresh_token = current_user.central_refresh_token
    access_token = current_user.central_token 
    central_url = current_user.central_url
    oath2_url = central_url + "/oauth2/token"
    api_test_url = central_url + "/configuration/v2/groups"

#is out token valid?
    qheaders = {
        "Content-Type":"application/json",
        "Authorization": "Bearer " + access_token,
        "limit": "1"
    }

    qparams = {
        "limit": 1,
        "offset": 0

    }

    if __debug__:
       print("Validating ACCESS TOKEN")

    response = requests.request("GET", api_test_url, headers=qheaders, params=qparams)

    if "error" in response.json():

      if __debug__:
        print("ACCESS TOKEN is INVALID or EXPIRED.  Refreshing tokens...")


      #refresh the token
      qparams = {
          "grant_type":"refresh_token",
          "client_id": clientID,
          "client_secret": client_secret,
          "refresh_token": refresh_token
      }

      response = requests.request("POST", oath2_url, params=qparams)

      if __debug__:
        print("DEBUG OUTPUT. Also updated in access_token,json")
        print(response.text.encode('utf8'))

      if "error" in response.json():

        if __debug__:
          print("UNABLE to refresh ACCESS TOKEN. REFRESH TOKEN, CLIENT ID or CLIENT SECRET INVALID")
        messages.error(request, 'Unable to connect to the Central API. Check values and try again.')

      else:
        # extract the new refresh token from the response
        current_user.central_token = response.json()['access_token']
        current_user.central_refresh_token = response.json()['refresh_token']
        current_user.save()

    else:
      if __debug__:
        print("ACCESS TOKEN is vlaid.  No action required.")
      if test:
        messages.success(request, 'Central API connection confirmed')

    return redirect(to='/profile/')

@login_required(login_url="/login/")
def update_sites(request):

    #call test_central to verify our connection and refresh the tokens if needed
    test_central(request,False)

    username = request.user.username

    #get the access token from the user profile
    current_user = request.user.profile

    clientID = current_user.central_clientID
    custID = current_user.central_custID
    client_secret = current_user.central_client_secret
    refresh_token = current_user.central_refresh_token
    access_token = current_user.central_token
    central_url = current_user.central_url
    get_sites_url = central_url + "/central/v2/sites"

    qheaders = {
        "Content-Type":"application/json",
        "Authorization": "Bearer " + access_token,
        "limit": "1000"
    }

    qparams = {
        "offset": 0,
        "limit": 1,
        "calculate_total": "true"
    }

    response = requests.request("GET", get_sites_url, headers=qheaders, params=qparams)

    if __debug__:
      print("------------------------------------")
      print(response.text.encode('utf8'))
      print("------------------------------------")

    total_sites = response.json()['total']
    print("total sites = ", total_sites);

#    dict_data=response.json()['sites']

#    if __debug__:
#      print(dict_data)


#    for dic_single in dict_data:
#      site=CentralSites()
#      site.key= username + dic_single['site_name']
#      site.username=username
#      site.address=dic_single['address']
#      site.city=dic_single['city']
#      site.country=dic_single['country']
#      site.latitude=dic_single['latitude']
#      site.longitude=dic_single['longitude']
#      site.site_id=dic_single['site_id']
#      site.site_name=dic_single['site_name']
#      site.state=dic_single['state']
#      site.tags=dic_single['tags']
#      site.zipcode=dic_single['zipcode']
#      site.save()


#    if total_sites > 1000 :
    loop_count = math.ceil(total_sites / 1000) -1
    print("loop count = ", loop_count);
    
    for x in range(0, loop_count+1):
        print("We're on time %d" % (x))
        print("Offset =  %d" % (1000 * x))

        qparams = {
            "offset": 1000 * x,
            "limit": 1000,
            "calculate_total": "true"
        }

        response = requests.request("GET", get_sites_url, headers=qheaders, params=qparams)

#        if __debug__:
#          print("------------------------------------")
#          print(response.text.encode('utf8'))
#          print("------------------------------------")

        dict_data=response.json()['sites']

        for dic_single in dict_data:
          site=CentralSites()
          site.customer_id = custID
#          site.key= username + dic_single['site_name']
#          site.username=username
          site.address=dic_single['address']
          site.associated_device_count=dic_single['associated_device_count']
          site.city=dic_single['city']
          site.country=dic_single['country']
          site.latitude=dic_single['latitude']
          site.longitude=dic_single['longitude']
          site.site_id=dic_single['site_id']
          site.site_name=dic_single['site_name']
          site.state=dic_single['state']
          site.tags=dic_single['tags']
          site.zipcode=dic_single['zipcode']
          site.last_refreshed = datetime.now()
          site.save()
    
    return


@login_required(login_url="/login/")
def update_tvariable(site_id, _sys_serial, _sys_lan_mac, variable, value):
  data_set = { "total": "1", "variables": { variable: value } } 
  data_dump  = json.dumps(data_set)
  data = json.loads(data_dump)

  if __debug__:
    print(data)

  #get the access token from the user profile
  current_user = request.user.profile
  access_token = current_user.central_token
  central_url = current_user.central_url

  #**********************************
  #make API call 
  #**********************************
  api_url = central_url + "/configuration/v1/devices/" + _sys_serial + "/template_variables"

  qheaders = { 
    "Content-Type":"application/json",
    "Authorization": "Bearer " + access_token,
  }   

  qparams = { 
  }   

  response = requests.request("POST", api_url, headers=qheaders, json=data)
    

  return

@login_required(login_url="/login/")
def update_tmdvariable(data):
  data_set = { "total": "1", "variables": { variable: value } } 
  data_dump  = json.dumps(data_set)
  data = json.loads(data_dump)

  if __debug__:
    print(data)

  #get the access token from the user profile
  current_user = request.user.profile
  access_token = current_user.central_token
  central_url = current_user.central_url

  #**********************************
  #make API call 
  #**********************************
  api_url = central_url + "/configuration/v1/devices/" + _sys_serial + "/template_variables"

  qheaders = { 
    "Content-Type":"application/json",
    "Authorization": "Bearer " + access_token,
  }   

  qparams = { 
  }   

  response = requests.request("POST", api_url, headers=qheaders, json=data)


@login_required(login_url="/login/")
def get_site_inventory(request,site, dev_type):

#  print(site+" "+ dev_type)

  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
      "offset": 0,
      "limit": 1000,
      "site": site,
      "calculate_total": "true"
  }

  if (dev_type == "AP"):
    query_url = central_url + "/monitoring/v2/aps"
    response = requests.request("GET", query_url, headers=qheaders, params=qparams)

  elif (dev_type == "SWITCH"):
    query_url = central_url + "/monitoring/v1/switches"
    response = requests.request("GET", query_url, headers=qheaders, params=qparams)

  elif (dev_type == "GW"):
    query_url = central_url + "/monitoring/v1/gateways"
    response = requests.request("GET", query_url, headers=qheaders, params=qparams)

  return response.json()
  
@login_required(login_url="/login/")
def get_variables(request, device_serial):


  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
      "device_serial": device_serial,
  }

  query_url = central_url + "/configuration/v1/devices/" + device_serial + "/template_variables"
  response = requests.request("GET", query_url, headers=qheaders, params=qparams)

  return response.json()

@login_required(login_url="/login/")
def get_stack_conductor(request, stack_name):


  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
      "hostname": stack_name,
  }

  query_url = central_url + "/monitoring/v1/switch_stacks"
  response = requests.request("GET", query_url, headers=qheaders, params=qparams)

  return response.json()['stacks'][0]['mac'] 

@login_required(login_url="/login/")
def set_variable(request, device_serial, variable, value ):

  data_set = { "total": 1, "variables": { variable: value } }
  data_dump  = json.dumps(data_set)
  data = json.loads(data_dump)

  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
      "device_serial": device_serial,
  }

  query_url = central_url + "/configuration/v1/devices/" + device_serial + "/template_variables"
  response = requests.request("PATCH", query_url, headers=qheaders, json=data)
  print("Set_variable response = ")
  print(response)
  print(response.encoding)
  print(response.text)
  
  return response.text

@login_required(login_url="/login/")
def get_autocommit(request, device_serial):


  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
      "device_serial": device_serial,
  }

  query_url = central_url + "/configuration/v1/auto_commit_state/devices" + device_serial
  response = requests.request("GET", query_url, headers=qheaders, params=qparams)

  return response.json()

@login_required(login_url="/login/")
def set_autocommit(request, state, device_serial):

  data_set = { "serials": [ device_serial ], "auto_commit_state": state }
  data_dump  = json.dumps(data_set)
  data = json.loads(data_dump)

  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
      "device_serial": device_serial,
  }

  query_url = central_url + "/configuration/v1/auto_commit_state/devices"
  response = requests.request("POST", query_url, headers=qheaders, params=qparams, json=data)
  return response # there is no json response for this API call

@login_required(login_url="/login/")
def get_device_config(request, device_serial):

  #call test_central to verify our connection and refresh the tokens if needed
  test_central(request,False)

  print("Device serial = " + device_serial)

  #get the access token from the user profile
  current_user = request.user.profile

  clientID = current_user.central_clientID
  client_secret = current_user.central_client_secret
  refresh_token = current_user.central_refresh_token
  access_token = current_user.central_token
  central_url = current_user.central_url

  qheaders = {
      "Content-Type":"application/json",
      "Authorization": "Bearer " + access_token,
  }

  qparams = {
  }

  query_url = central_url + "/configuration/v1/devices/" + device_serial + "/configuration"
  response = requests.request("GET", query_url, headers=qheaders )
#  print(response)
#  print(response.encoding)
#  print(response.text)
  return response.text
