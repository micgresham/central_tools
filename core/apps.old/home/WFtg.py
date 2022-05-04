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
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage

import requests
import json
import urllib.parse
import time
import math

from .models import CentralSites



#--------------------------------------------------
#common API functions from common_views 
#--------------------------------------------------
from apps.home.common_views import get_site_inventory
from apps.home.common_views import test_central
from apps.home.common_views import update_sites
from apps.home.common_views import update_tvariable
from apps.home.common_views import update_tmdvariable
from apps.home.common_views import get_variables
from apps.home.common_views import get_stack_conductor
from apps.home.common_views import set_variable
from apps.home.common_views import get_autocommit
from apps.home.common_views import set_autocommit


#-----------------------------------------
#Forms for the workflow
#-----------------------------------------

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelForm
from django.utils.safestring import mark_safe

class PlainTextWidgetWithHiddenCopy(forms.Widget):
    def render(self, name, value, attrs, renderer=None):
        if hasattr(self, 'initial'):
            value = self.initial

        return mark_safe(
            '<b>' + (str(value) if value is not None else '-') +
            f"</b><input type='hidden' name='{name}' value='{value}'><br>"
        )

class CreateTgroupForm(forms.Form):
    ARCH_CHOICE =(
       ("Instant", "Instant"),
       ("AOS10", "AOS10"),
    )
    AP_ROLE_CHOICE =(
       ("Standard", "Standard"),
       ("Microbranch", "Microbranch"),
    )
    GW_ROLE_CHOICE =(
       ("BranchGateway", "Branch Gateway"),
       ("VPNConcentrator", "VPN Concentrator"),
       ("WLANGateway", "WLAN Gateway"),
    )
    DEV_TYPE_CHOICE =(
       ("AccessPoints", "Access Points"),
       ("Gateways", "Gateways"),
       ("Switches", "Switches"),
    )
    SW_TYPE_CHOICE =[
       ("AOS_S", "AOS-S"),
       ("AOS_CX", "CX"),
    ]
    TGROUP_CHOICE =(
       ("Wired", "Wired"),
       ("Wireless", "IAP and Gateway"),
    )
    TDEV_TYPE_CHOICE =(
       ("CX", "CX"),
       ("ArubaSwitch", "Aruba Switch"),
       ("IAP", "IAP"),
       ("MobilityController", "Mobility Controller"),
    )


    Tgroup_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Template Group Name', 'class': 'form-control',
       }))

    template = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    Tmodel = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': '6300', 'class': 'form-control',
       }))

    Tversion = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ALL', 'class': 'form-control',
       }))

    TDevType = forms.ChoiceField(
         required=True,
         choices = TDEV_TYPE_CHOICE,
         )

    TgroupTypes = forms.MultipleChoiceField(
         required=True,
         choices = TGROUP_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )
    
    AllowedDeviceTypes = forms.MultipleChoiceField(
         choices = DEV_TYPE_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )
    Architecture = forms.ChoiceField(choices = ARCH_CHOICE)
    ApNetworkRole = forms.ChoiceField(choices = AP_ROLE_CHOICE,
         widget=forms.Select(),
         )
    GwNetworkRole = forms.ChoiceField(choices = GW_ROLE_CHOICE,
         widget=forms.Select(),
         )
    AllowedSwitchTypes = forms.MultipleChoiceField(
         required='required',
         choices = SW_TYPE_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )

class CreateMTgroupForm(forms.Form):
    ARCH_CHOICE =(
       ("Instant", "Instant"),
       ("AOS10", "AOS10"),
    )
    AP_ROLE_CHOICE =(
       ("Standard", "Standard"),
       ("Microbranch", "Microbranch"),
    )
    GW_ROLE_CHOICE =(
       ("BranchGateway", "Branch Gateway"),
       ("VPNConcentrator", "VPN Concentrator"),
       ("WLANGateway", "WLAN Gateway"),
    )
    DEV_TYPE_CHOICE =(
       ("AccessPoints", "Access Points"),
       ("Gateways", "Gateways"),
       ("Switches", "Switches"),
    )
    SW_TYPE_CHOICE =[
       ("AOS_S", "AOS-S"),
       ("AOS_CX", "CX"),
    ]
    TGROUP_CHOICE =(
       ("Wired", "Wired"),
       ("Wireless", "IAP and Gateway"),
    )
    TDEV_TYPE_CHOICE =(
       ("CX", "CX"),
       ("ArubaSwitch", "Aruba Switch"),
       ("IAP", "IAP"),
       ("MobilityController", "Mobility Controller"),
    )


    Tgroup_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Template Group Name', 'class': 'form-control',
       }))

    Tgroup_range = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Template Name Range', 'class': 'form-control',
       }))

    template = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    Tmodel = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': '6300', 'class': 'form-control',
       }))

    Tversion = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ALL', 'class': 'form-control',
       }))

    TDevType = forms.ChoiceField(
         required=True,
         choices = TDEV_TYPE_CHOICE,
         )

    TgroupTypes = forms.MultipleChoiceField(
         required=True,
         choices = TGROUP_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )
    
    AllowedDeviceTypes = forms.MultipleChoiceField(
         choices = DEV_TYPE_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )
    Architecture = forms.ChoiceField(choices = ARCH_CHOICE)
    ApNetworkRole = forms.ChoiceField(choices = AP_ROLE_CHOICE,
         widget=forms.Select(),
         )
    GwNetworkRole = forms.ChoiceField(choices = GW_ROLE_CHOICE,
         widget=forms.Select(),
         )
    AllowedSwitchTypes = forms.MultipleChoiceField(
         required='required',
         choices = SW_TYPE_CHOICE,
         widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
         )

class FilterSiteForm(ModelForm):

    site_name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zipcode = forms.CharField(required=False)

    class Meta:

       model = CentralSites 
       fields = (
         'site_name',
         'address',
         'city',
         'state',
         'zipcode'
     )


#-----------------------------------------
#Views for the workflow
#-----------------------------------------

@login_required(login_url="/login/")
def create_tgroup(request):

    if request.method == 'POST':
      if __debug__:
        print("create_tgroup POST")

      form = CreateTgroupForm(request.POST, request.FILES)

      if form.is_valid():

         myfile = request.FILES['template']
         fs = FileSystemStorage()
         filename = fs.save('templates/' + myfile.name, myfile)

         TgroupName = request.POST.get('Tgroup_name')
         TgroupTypes = request.POST.getlist('TgroupTypes')
         TDevType = request.POST.get('TDevType')
         Tmodel = request.POST.get('Tmodel')
         Tversion = request.POST.get('Tversion')
         Architecture = request.POST.get('Architecture')
         AllowedDeviceTypes = request.POST.getlist('AllowedDeviceTypes')
         AllowedSwitchTypes = request.POST.getlist('AllowedSwitchTypes')
         GwNetworkRole = request.POST.get('GwNetworkRole')
         ApNetworkRole = request.POST.get('ApNetworkRole')

         if __debug__:
           print(myfile.name)

         #Create the initial JSON structure

# for the new API (internal)
         data_set = { "group": TgroupName, "group_attributes": { "template_info": { "Wired": True, "Wireless": True }, "group_properties": { "AllowedDevTypes": AllowedDeviceTypes, "Architecture": Architecture, "ApNetworkRole": ApNetworkRole, "GwNetworkRole": GwNetworkRole, "AllowedSwitchTypes": AllowedSwitchTypes } } }
#         data_set = { "group": TgroupName, "group_attributes": { "group_password": "" ,"template_info": { "Wired": True, "Wireless": True } } }
         data_dump  = json.dumps(data_set)
         data = json.loads(data_dump)

         if __debug__:
           print(data)

         #call test_central to verify our connection and refresh the tokens if needed
         test_central(request,False)

         #get the access token from the user profile
         current_user = request.user.profile
         access_token = current_user.central_token
         central_url = current_user.central_url

         #**********************************
         #make API call to create the group         
         #**********************************
         api_url = central_url + "/configuration/v3/groups"

         #is out token valid?
         qheaders = {
           "Content-Type":"application/json",
           "Authorization": "Bearer " + access_token,
         }

         qparams = {
           "limit": 1,
           "offset": 0
         }

         response = requests.request("POST", api_url, headers=qheaders, json=data)
         
         if __debug__:
           print(api_url)
           print(response)
           print(response.text.encode('utf8'))
 
         if "Created" in response.json():
            messages.success(request, 'Group ' + TgroupName + ' created ')

            #**********************************
            #make API call to add the template to the group         
            #**********************************
            api_url = central_url + "/configuration/v1/groups/" + TgroupName + "/templates"

            # do not put 'Content-Type': 'application/json' in the headers.  It will cause fordata errors
            qheaders={
               "Authorization": "Bearer " + access_token,
            }
            qparams={
                "name": urllib.parse.quote_plus(myfile.name),
                "device_type": TDevType,
                "version": Tversion,
                "model": Tmodel,
            }
            qpayload={}
            qfiles=[
               ('template',(myfile.name,open(settings.MEDIA_ROOT + '/' + filename,'rb'),'text/plain'))
            ]

            # call the API and send the template file to the group
            response = requests.request("POST", api_url, params=qparams, headers=qheaders, data=qpayload, files=qfiles)
            if "Created" in response.json():
               messages.success(request, 'Template ' + myfile.name + ' uploaded. ')
            else:
               messages.warning(request, 'Template ' + myfile.name + " not uploaded to group " + TgroupName)
                
            if __debug__:
              print(response.text.encode('utf8'))

            # return from whence thy came
            context = {}
            context['form'] = CreateTgroupForm()
            return render( request, "home/create_tgroup.html", context)

         else:
            print("NOT CREATED")
            messages.warning(request, 'Group ' + TgroupName + ' creation failed. ' + response.text)
            messages.warning(request, 'URL: ' + api_url)
 
            context = {}
            context['form'] = CreateTgroupForm()
            return render( request, "home/create_tgroup.html", context)
      else:
         context = {}
         context['form'] = CreateTgroupForm()
         return render( request, "home/create_tgroup.html", context)

    else:
      context = {}
      context['form'] = CreateTgroupForm()
      return render( request, "home/create_tgroup.html", context)



# -------------------------
# create template multi groups
# -------------------------

def mixrange(s):
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l,h = map(int, i.split('-'))
            r+= range(l,h+1)
    return r



@login_required(login_url="/login/")
def create_mtgroup(request):

    if request.method == 'POST':
      if __debug__:
        print("create_tgroup POST")

      form = CreateTgroupForm(request.POST, request.FILES)

      if form.is_valid():

         myfile = request.FILES['template']
         fs = FileSystemStorage()
         filename = fs.save('templates/' + myfile.name, myfile)

         TgroupName = request.POST.get('Tgroup_name')
         TgroupRange = request.POST.get('Tgroup_range')
         TgroupTypes = request.POST.getlist('TgroupTypes')
         TDevType = request.POST.get('TDevType')
         Tmodel = request.POST.get('Tmodel')
         Tversion = request.POST.get('Tversion')
         Architecture = request.POST.get('Architecture')
         AllowedDeviceTypes = request.POST.getlist('AllowedDeviceTypes')
         AllowedSwitchTypes = request.POST.getlist('AllowedSwitchTypes')
         GwNetworkRole = request.POST.get('GwNetworkRole')
         ApNetworkRole = request.POST.get('ApNetworkRole')

         if __debug__:
           print(myfile.name)

         #create the templates
         data_set = dict() 
         for i in mixrange(TgroupRange):
            
            MTgroupName = TgroupName.format(i)
            #Create the initial JSON structure
            # for Central 2.5.4 and later API
            data_set[MTgroupName] = { "group": MTgroupName, "group_attributes": { "template_info": { "Wired": True, "Wireless": True }, "group_properties": { "AllowedDevTypes": AllowedDeviceTypes, "Architecture": Architecture, "ApNetworkRole": ApNetworkRole, "GwNetworkRole": GwNetworkRole, "AllowedSwitchTypes": AllowedSwitchTypes } } }

            # for Central version prior to 2.5.4 - no longer used
#            data_set[MTgroupName] = { "group": MTgroupName, "group_attributes": { "group_password": "" ,"template_info": { "Wired": True, "Wireless": True } } }
            print(i)

         for key, values in data_set.items():
            print('Key :: ', key)
            data_dump  = json.dumps(values)
            data = json.loads(data_dump)
            if __debug__:
              print(data)

         #call test_central to verify our connection and refresh the tokens if needed
         test_central(request,False)

         #get the access token from the user profile
         current_user = request.user.profile
         access_token = current_user.central_token
         central_url = current_user.central_url

         #**********************************
         #loop over the range and make API call to create the group         
         #**********************************
         for key, values in data_set.items():
            print('Key :: ', key)
            data_dump  = json.dumps(values)
            data = json.loads(data_dump)
            if __debug__:
              print(data)
            api_url = central_url + "/configuration/v3/groups"

            #is out token valid?
            qheaders = {
              "Content-Type":"application/json",
              "Authorization": "Bearer " + access_token,
            }
   
            qparams = {
              "limit": 1,
              "offset": 0
            }

            response = requests.request("POST", api_url, headers=qheaders, json=data)
            
            if __debug__:
              print(api_url)
              print(response)
              print(response.text.encode('utf8'))
 
            if "Created" in response.json():
               messages.success(request, 'Group ' + key + ' created ')
   
               #**********************************
               #make API call to add the template to the group         
               #**********************************
               api_url = central_url + "/configuration/v1/groups/" + key + "/templates"
   
               # do not put 'Content-Type': 'application/json' in the headers.  It will cause fordata errors
               qheaders={
                  "Authorization": "Bearer " + access_token,
               }
               qparams={
                   "name": urllib.parse.quote_plus(myfile.name),
# old name                   "name": key,
                   "device_type": TDevType,
                   "version": Tversion,
                   "model": Tmodel,
               }
               qpayload={}
               qfiles=[
                  ('template',(myfile.name,open(settings.MEDIA_ROOT + '/' + filename,'rb'),'text/plain'))
               ]
   
               # call the API and send the template file to the group
               time.sleep(1)
               response = requests.request("POST", api_url, params=qparams, headers=qheaders, data=qpayload, files=qfiles)
               if "Created" in response.json():
                  messages.success(request, 'Template ' + myfile.name + ' uploaded. ')
               else:
                  messages.warning(request, 'Template ' + myfile.name + " not uploaded to group " + key)
                
               if __debug__:
                 print(response.text.encode('utf8'))
               
               time.sleep(1)
            else:
               print("NOT CREATED")
               messages.warning(request, 'Group ' + TgroupName + ' creation failed. ' + response.text)
               messages.warning(request, 'URL: ' + api_url)
 
         context = {}
         context['form'] = CreateMTgroupForm()
         return render( request, "home/create_mtgroup.html", context)
      else:
         context = {}
         context['form'] = CreateMTgroupForm()
         return render( request, "home/create_mtgroup.html", context)

    else:
      context = {}
      context['form'] = CreateMTgroupForm()
      return render( request, "home/create_mtgroup.html", context)


@login_required(login_url="/login/")
def show_sites(request):

  username = request.user.username

  # request.session['site_refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') 
  # we only want to reload the sites list from central once every 24 hours since it can takes so long
  if  not "site_refresh" in request.session:
    print("I did not find site_refresh in the session variables")
    request.session['site_refresh'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    update_sites(request)
  else:
    print("I found site_refresh in the session variables")
    #has it been 24 hours?
    dts = datetime.strptime(request.session['site_refresh'], '%Y-%m-%d %H:%M:%S.%f')
    if (dts + timedelta(days=1) < datetime.now()):
       print("It has been more than a day. Refreshing the site list") 
       update_sites(request)


  if request.method == 'POST':
    form = FilterSiteForm(request.POST)
    if form.is_valid():
      dict_data = CentralSites.objects.filter(customer_id__contains=request.user.profile.central_custID).order_by('site_name')
      if form.data['state']:
         dict_data = dict_data.filter(state__contains=form.data['state'])
      if form.data['city']:
         dict_data = dict_data.filter(city__contains=form.data['city'])
      if form.data['zip']:
         dict_data = dict_data.filter(zipcode__contains=form.data['zip'])
      if form.data['address']:
         dict_data = dict_data.filter(address__contains=form.data['address'])
      if form.data['site_name']:
         dict_data = dict_data.filter(site_name__contains=form.data['site_name'])
    else:
      dict_data = CentralSites.objects.filter(customer_id__contains=request.user.profile.central_custID).order_by('site_name')
      
    context = {'query_results': dict_data}
    return render( request, "home/show_sites.html", context)
  else:
    dict_data = CentralSites.objects.filter(customer_id__contains=request.user.profile.central_custID).order_by('site_name')
    context = {'query_results': dict_data}
    return render( request, "home/show_sites.html", context)

