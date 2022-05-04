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
from apps.home.common_views import get_device_config


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

class WFcfg_SelectSiteForm(forms.Form):

    device_choices = (
        ("IAP", "IAP"),
        ("SWITCH", "SWITCH"),
#        ("GW", "GATEWAY"),
    )

    site_name = forms.ModelChoiceField(queryset=CentralSites.objects.none(),
                to_field_name="site_name"
           )
    dev_type = forms.ChoiceField(choices = device_choices)
    stage = forms.CharField(widget=forms.HiddenInput(), initial="1")



    def __init__(self, *args, customer_id='%', **kwargs):
        super(WFcfg_SelectSiteForm, self).__init__(*args, **kwargs)
        self.fields['site_name'].queryset = CentralSites.objects.filter(customer_id__contains=customer_id).order_by('site_name')
        self.fields['site_name'].label_from_instance = lambda obj: "%s" % obj.site_name

class WFcfg_SelectDeviceForm(forms.Form):            

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_name = forms.ChoiceField()
    stage = forms.CharField(widget=forms.HiddenInput(), initial="2")
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="2")

    def __init__(self, *args, site_name="", dev_type="", device_names=[], **kwargs):

        super(WFcfg_SelectDeviceForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.fields['device_name'].choices = device_names

class WFcfg_ShowConfigeDeviceForm(forms.Form):

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_serial = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="2")

    stage = forms.CharField(widget=forms.HiddenInput(), initial="3")



    def __init__(self, *args, site_name="", dev_type="", device_name="", device_serial="", **kwargs):

        super(WFcfg_ShowConfigeDeviceForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.initial['device_name'] = device_name
        self.initial['device_serial'] = device_serial


#-----------------------------------------
#Views for the workflow
#-----------------------------------------

@login_required(login_url="/login/")
def WFcfg_select_site(request):

  username = request.user.username

  if request.method == 'POST': #a site and dvice type has been selected, now select the variables
    context = {}
    stage = request.POST.get('stage')
    if (stage == '1'):
       print("STAGE 1 PROCESSING")
       dev_type = request.POST.get('dev_type')
       site = request.POST.get('site_name')
       device_set = list()
       if (dev_type == 'IAP'):
         queryset = get_site_inventory(request,site, "AP")
         if (queryset['total'] == 0):
            messages.warning(request, 'Selected site and device type has no members.')
            context = {'submit_button': "Next"}
            context['form']= WFcfg_SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WFcfg.html", context)

         for each in queryset['aps']:
            if (each['serial'],each['name']) not in device_set:
               device_set.append(([each['serial'],each['name']],each['name']+' (SN:'+each['serial']+')'))

         context = {'submit_button': "Next"}
         context['form']= WFcfg_SelectDeviceForm(site_name=request.POST.get('site_name'),
                                         dev_type=request.POST.get('dev_type'),
                                         device_names=device_set)

       else:
         queryset = get_site_inventory(request,site, "SWITCH")
         if (queryset['total'] == 0):
            messages.warning(request, 'Selected site and device type has no members.')
            context = {'submit_button': "Next"}
            context['form']= WFcfg_SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WFcfg.html", context)

         device_serial = queryset['switches'][0]['serial']
         for each in queryset['switches']:
            if (each['serial'],each['name']) not in device_set:
               device_set.append(([each['serial'],each['name']],each['name']+' (SN:'+each['serial']+')'))

         context = {'submit_button': "Next"}
         context['form']= WFcfg_SelectDeviceForm(site_name=request.POST.get('site_name'),
                                         dev_type=request.POST.get('dev_type'),
                                         device_names=device_set)

       return render( request, "home/WFcfg.html", context)

    elif (stage == '2'):
       print("STAGE 2 PROCESSING")
       dev_type = request.POST.get('dev_type')
       site = request.POST.get('site_name')
       change_type = request.POST.get('change_type')
       print("change type 2")
       device = request.POST.get('device_name').translate({ord('\''): None}).strip('][').split(', ')
       device_serial = device[0]
       device_name = device[1]

       config_text = get_device_config(request,device_serial)

       fn_url = settings.MEDIA_URL + 'configs/' + device_name + "_" + device_serial + ".cfg"
       fn = settings.MEDIA_ROOT + '/' + 'configs/' + device_name + "_" + device_serial + ".cfg"
       print(fn)
       with open(fn,"w") as file:
         file.write(config_text)

       context = {'download_URL' : fn_url, 'config' : config_text}

       context['form']= WFcfg_ShowConfigeDeviceForm(site_name=site,
                                         dev_type = dev_type,
                                         device_name = device_name,
                                         device_serial = device_serial)

       return render( request, "home/WFcfg.html", context)

    elif (stage == '3'):
       print("STAGE 3 PROCESSING")

    elif (stage == '4'):
       print("STAGE 1 PROCESSING")

    else:
       print("NO STAGE PROCESSING")
       context = {'submit_button': "Next"}
       context['form']= WFcfg_SelectSiteForm(customer_id=request.user.profile.central_custID)
       return render( request, "home/WFcfg.html", context)

  else:
    context = {'submit_button': "Next"}
    context['form']= WFcfg_SelectSiteForm(customer_id=request.user.profile.central_custID)
    return render( request, "home/WFcfg.html", context)


