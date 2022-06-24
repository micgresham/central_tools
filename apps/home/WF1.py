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
from .pymenu import Menu



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

class WF1SelectSiteForm(forms.Form):

    device_choices = (
        ("IAP", "IAP"),
        ("SWITCH", "SWITCH"),
#        ("GW", "GATEWAY"),
    )

    change_choices = (
        ("2", "DEVICE"),
        ("1", "TEMPLATE"),
        ("3", "STACK"),
        ("4", "VC"),
    )

    site_name = forms.ModelChoiceField(queryset=CentralSites.objects.none(),
                to_field_name="site_name"
#               required=False,
#               widget=forms.Select(
#                   attrs={
#			'onchange': 'load_sub_codes();',
#                   }
           )
    dev_type = forms.ChoiceField(choices = device_choices)
    change_type = forms.ChoiceField(choices = change_choices)
    stage = forms.CharField(widget=forms.HiddenInput(), initial="1")


#    class Meta:      
#        model = CentralSites
#        fields = ['site_name']

    def __init__(self, *args, customer_id='%', **kwargs):
        super(WF1SelectSiteForm, self).__init__(*args, **kwargs)
        self.fields['site_name'].queryset = CentralSites.objects.filter(customer_id__contains=customer_id).order_by('site_name')
        self.fields['site_name'].label_from_instance = lambda obj: "%s" % obj.site_name

class WF1SelectTemplateForm(forms.Form):            

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    change_type = forms.CharField(widget=forms.HiddenInput())
    template_name = forms.ChoiceField()
    stage = forms.CharField(widget=forms.HiddenInput(), initial="2")
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="1")

    def __init__(self, *args, site_name="", dev_type="", template_names=[], **kwargs):

        super(WF1SelectTemplateForm, self).__init__(*args, **kwargs)
#        print(args)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.fields['template_name'].choices = template_names
#        print(template_names)

class WF1SelectDeviceForm(forms.Form):            

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_name = forms.ChoiceField()
    stage = forms.CharField(widget=forms.HiddenInput(), initial="2")
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="2")

    def __init__(self, *args, site_name="", dev_type="", device_names=[], **kwargs):

        super(WF1SelectDeviceForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.fields['device_name'].choices = device_names

class WF1SelectStackForm(forms.Form):            

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    stack_name = forms.ChoiceField()
    stage = forms.CharField(widget=forms.HiddenInput(), initial="2")
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="3")

    def __init__(self, *args, site_name="", dev_type="", stack_names=[], **kwargs):

        super(WF1SelectStackForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.fields['stack_name'].choices = stack_names

class WF1SelectVCForm(forms.Form):            

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    swarm_name = forms.ChoiceField()
    stage = forms.CharField(widget=forms.HiddenInput(), initial="2")
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="4")

    def __init__(self, *args, site_name="", dev_type="", swarm_names=[], **kwargs):

        super(WF1SelectVCForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.fields['swarm_name'].choices = swarm_names

class WF1SelectVariableTemplateForm(forms.Form):            

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    template_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="1")
    variable = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    value = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'NEW VALUE', 'class': 'form-control',
       }))

    stage = forms.CharField(widget=forms.HiddenInput(), initial="3")
    device_serial = forms.CharField(widget=forms.HiddenInput())
    override_commit_off = forms.BooleanField(required=False)



    def __init__(self, *args, site_name="", dev_type="", template_name="", variables=[], device_serial="", **kwargs):

        super(WF1SelectVariableTemplateForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.initial['template_name'] = template_name
        self.initial['device_serial'] = device_serial
        self.fields['variable'].choices = variables

class WF1SelectVariableDeviceForm(forms.Form):

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_serial = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    change_type = forms.CharField(widget=forms.HiddenInput(), initial="2")
    variable = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    value = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'NEW VALUE', 'class': 'form-control',
       }))

    stage = forms.CharField(widget=forms.HiddenInput(), initial="3")
    override_commit_off = forms.BooleanField(required=False)



    def __init__(self, *args, site_name="", dev_type="", device_name="", variables=[], device_serial="", **kwargs):

        super(WF1SelectVariableDeviceForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.initial['device_name'] = device_name
        self.initial['device_serial'] = device_serial
        self.fields['variable'].choices = variables

class WF1SelectVariableStackForm(forms.Form):

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    stack_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    stack_id = forms.CharField(widget=forms.HiddenInput(), initial="bob")
    serials = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    variable = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    value = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'NEW VALUE', 'class': 'form-control',
       }))

    change_type = forms.CharField(widget=forms.HiddenInput(), initial="3")
    stage = forms.CharField(widget=forms.HiddenInput(), initial="3")
    override_commit_off = forms.BooleanField(required=False)



    def __init__(self, *args, site_name="", dev_type="", stack_name="", stack_id="",  serials=[], variables=[],  **kwargs):

        super(WF1SelectVariableStackForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.initial['stack_name'] = stack_name
        self.initial['stack_id'] = stack_id
        self.fields['variable'].choices = variables
        self.initial['serials'] = ', '.join([str(elem[0]) for elem in serials])


class WF1SelectVariableVCForm(forms.Form):

    site_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    dev_type = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    device_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    swarm_name = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    swarm_id = forms.CharField(widget=forms.HiddenInput(), initial="bob")
    serials = forms.CharField(widget=PlainTextWidgetWithHiddenCopy(attrs={'class=': 'mb-3 form-control'}))
    variable = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    value = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'NEW VALUE', 'class': 'form-control',
       }))

    change_type = forms.CharField(widget=forms.HiddenInput(), initial="4")
    stage = forms.CharField(widget=forms.HiddenInput(), initial="3")
    override_commit_off = forms.BooleanField(required=False)



    def __init__(self, *args, site_name="", dev_type="", swarm_name="", swarm_id="",  serials=[], variables=[],  **kwargs):

        super(WF1SelectVariableVCForm, self).__init__(*args, **kwargs)
        self.initial['site_name'] = site_name
        self.initial['dev_type'] = dev_type
        self.initial['swarm_name'] = swarm_name
        self.initial['swarm_id'] = swarm_id
        self.fields['variable'].choices = variables
        self.initial['serials'] = ', '.join([str(elem[0]) for elem in serials])


#-----------------------------------------
#Views for the workflow
#-----------------------------------------

@login_required(login_url="/login/")
def WF1select_site(request):


  if request.method == 'POST': #a site and dvice type has been selected, now select the variables
    context = {}
    menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
    context['menu'] = menu
    stage = request.POST.get('stage')
    if (stage == '1'):
       form = WF1SelectTemplateForm(request.POST)
       print("STAGE 1 PROCESSING")
       dev_type = request.POST.get('dev_type')
       site = request.POST.get('site_name')
       change_type = request.POST.get('change_type')
       if (change_type == "1"): #change type is for all devices in a template
         template_set = list()
         if (dev_type == 'IAP'):
           queryset = get_site_inventory(request,site, "AP")
           if (queryset['total'] == 0):
              messages.warning(request, 'Selected site and device type has no members.')
              context = {'submit_button': "Next"}
              menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
              context['menu'] = menu
              context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
              return render( request, "home/WF1.html", context)

           device_serial = queryset['aps'][0]['serial']


           for each in queryset['aps']:
              if (each['group_name'],each['group_name']) not in template_set:
                 template_set.append((each['group_name'],each['group_name']))
  
         else:
           queryset = get_site_inventory(request,site, "SWITCH")
           if (queryset['total'] == 0):
              messages.warning(request, 'Selected site and device type has no members.')
              context = {'submit_button': "Next"}
              menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
              context['menu'] = menu
              context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
              return render( request, "home/WF1.html", context)

           device_serial = queryset['switches'][0]['serial']
           for each in queryset['switches']:
              if (each['group_name'],each['group_name']) not in template_set:
                 template_set.append((each['group_name'],each['group_name']))

         context = {'submit_button': "Next"}
         menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
         context['menu'] = menu
         context['form']= WF1SelectTemplateForm(site_name=request.POST.get('site_name'),
                                           dev_type=request.POST.get('dev_type'),
                                           template_names=template_set)
       elif (change_type == "2"): # change type (2) is for an individual device
         device_set = list()
         if (dev_type == 'IAP'):
           queryset = get_site_inventory(request,site, "AP")
           if (queryset['total'] == 0):
              messages.warning(request, 'Selected site and device type has no members.')
              context = {'submit_button': "Next"}
              menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
              context['menu'] = menu
              context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
              return render( request, "home/WF1.html", context)

           for each in queryset['aps']:
              if (each['serial'],each['name']) not in device_set:
                 device_set.append(([each['serial'],each['name']],each['name']+' (SN:'+each['serial']+')'))

           context = {'submit_button': "Next"}
           menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
           context['menu'] = menu
           context['form']= WF1SelectDeviceForm(site_name=request.POST.get('site_name'),
                                           dev_type=request.POST.get('dev_type'),
                                           device_names=device_set)
  
         else:
           queryset = get_site_inventory(request,site, "SWITCH")
           if (queryset['total'] == 0):
              messages.warning(request, 'Selected site and device type has no members.')
              context = {'submit_button': "Next"}
              menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
              context['menu'] = menu
              context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
              return render( request, "home/WF1.html", context)

           device_serial = queryset['switches'][0]['serial']
           for each in queryset['switches']:
              if (each['serial'],each['name']) not in device_set:
                 device_set.append(([each['serial'],each['name']],each['name']+' (SN:'+each['serial']+')'))

           context = {'submit_button': "Next"}
           menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
           context['menu'] = menu
           context['form']= WF1SelectDeviceForm(site_name=request.POST.get('site_name'),
                                           dev_type=request.POST.get('dev_type'),
                                           device_names=device_set)
       elif (change_type == "3"): # change type (3) is for all devices in a stack
         stack_set = list()
         if (dev_type == 'IAP'):
            messages.warning(request, 'Bad selection. APs cannot be in a stack')
            context = {'submit_button': "Next"}
            menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
            context['menu'] = menu
            context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WF1.html", context)
         else: # switch stacks
           queryset = get_site_inventory(request,site, "SWITCH")
           if (queryset['total'] == 0):
              messages.warning(request, 'Selected site and device type has no members.')
              context = {'submit_button': "Next"}
              menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
              context['menu'] = menu
              context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
              return render( request, "home/WF1.html", context)

           for each in queryset['switches']:
              if ([each['stack_id'],each['name']],each['name']) not in stack_set:
                 stack_set.append(([each['stack_id'],each['name']],each['name']))

           context = {'submit_button': "Next"}
           menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
           context['menu'] = menu
           context['form']= WF1SelectStackForm(site_name=request.POST.get('site_name'),
                                           dev_type=request.POST.get('dev_type'),
                                           stack_names=stack_set)
       else: # change type (4) is for an AP virtual controller (VC) swarm
         swarm_set = list()
         if (dev_type == 'SWITCH'):
            messages.warning(request, 'Bad selection. SWITCHES cannot be in a VC')
            context = {'submit_button': "Next"}
            menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
            context['menu'] = menu
            context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WF1.html", context)
         else: # IAP swarm
           queryset = get_site_inventory(request,site, "AP")
           if (queryset['total'] == 0):
              messages.warning(request, 'Selected site and device type has no members.')
              context = {'submit_button': "Next"}
              menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
              context['menu'] = menu
              context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
              return render( request, "home/WF1.html", context)

           for each in queryset['aps']:
              if ([each['swarm_id'],each['swarm_name']],each['swarm_name']) not in swarm_set:
                 swarm_set.append(([each['swarm_id'],each['swarm_name']],each['swarm_name']))

           context = {}
           menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
           context['menu'] = menu
           context = {'submit_button': "Next"}
           context['form']= WF1SelectVCForm(site_name=request.POST.get('site_name'),
                                           dev_type=request.POST.get('dev_type'),
                                           swarm_names=swarm_set)

       return render( request, "home/WF1.html", context)

    elif (stage == '2'):
       print("STAGE 2 PROCESSING")
       dev_type = request.POST.get('dev_type')
       site = request.POST.get('site_name')
       change_type = request.POST.get('change_type')
       if (change_type == "1"): #change type is for all devices in a template
         template_name = request.POST.get('template_name')
         if (dev_type == 'IAP'):
            queryset = get_site_inventory(request,site, "AP")
            template_set = list()
            for each in queryset['aps']:
               if (template_name == each['group_name']):
                 template_set.append((each['serial'],each['name']))
        
         else:
            queryset = get_site_inventory(request,site, "SWITCH")
            template_set = list()
            for each in queryset['switches']:
               if (template_name == each['group_name']):
                 template_set.append((each['serial'],each['name']))

         device_serial = template_set[0][0]
         queryset = get_variables(request, device_serial)
 
         variable_set = list()
         if (variable_set):         
           for each in queryset['data']['variables']:
               variable_set.append((each,each + ' (' + str(queryset['data']['variables'][each]) + ')'))
            
       
         context = {'submit_button': "Submit"}
         menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
         context['menu'] = menu
         context['form']= WF1SelectVariableTemplateForm(site_name=request.POST.get('site_name'),
                                          dev_type=request.POST.get('dev_type'),
                                          template_name = template_name,
                                          variables=variable_set,
                                          device_serial = device_serial)
         return render( request, "home/WF1.html", context)

       elif (change_type == "2"): # change type (2) is for an individual device
         print("change type 2")
         device = request.POST.get('device_name').translate({ord('\''): None}).strip('][').split(', ')
         device_serial = device[0]
         device_name = device[1]

         queryset = get_variables(request, device_serial)
         
         if not queryset:  # no variables defined for the device
            messages.warning(request, 'No variables define for device ' + device_name + '(' + device_serial + ')')
            context = {'submit_button': "Next"}
            menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
            context['menu'] = menu
            context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WF1.html", context)
           

         variable_set = list()
         for each in queryset['data']['variables']:
             variable_set.append((each,each + ' (' + str(queryset['data']['variables'][each]) + ')'))

         context = {'submit_button': "Submit"}
         menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
         context['menu'] = menu
         context['form']= WF1SelectVariableDeviceForm(site_name=request.POST.get('site_name'),
                                          dev_type=request.POST.get('dev_type'),
                                          device_name = device_name,
                                          variables=variable_set,
                                          device_serial = device_serial)
         return render( request, "home/WF1.html", context)

       elif (change_type == "3"): # change type (3) is for a switch stack
         print("change type 3")
         stack = request.POST.get('stack_name').translate({ord('\''): None}).strip('][').split(', ')
         stack_id = stack[0]
         stack_name = stack[1]
         print(stack_name)
         conductor_mac  = get_stack_conductor(request,stack_name) # we will need the later
         print('conductor_mac = ' + conductor_mac)


         queryset = get_site_inventory(request,site, "SWITCH")
         print('---------------------')
         template_set = list()
         for each in queryset['switches']:
            if (stack_id == each['stack_id']):
              template_set.append((each['serial'],each['name']))
              if (conductor_mac == each['macaddr']):
                 print('*****Found the conductor with serial # ' + each['serial'])
                 device_serial = each['serial']

         queryset = get_variables(request, device_serial)
         print(queryset)
         if not queryset:  # no variables defined
            messages.warning(request, 'No variables define for stack '+ stack_name)
            context = {'submit_button': "Next"}
            menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
            context['menu'] = menu
            context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WF1.html", context)
         
         variable_set = list()
         for each in queryset['data']['variables']:
             variable_set.append((each,each + ' (' + str(queryset['data']['variables'][each]) + ')'))

         context['submit_button'] = "Submit"
         context['form']= WF1SelectVariableStackForm(site_name=request.POST.get('site_name'),
                                          dev_type=request.POST.get('dev_type'),
                                          stack_name = stack_name,
                                          stack_id = stack_id,
                                          variables=variable_set,
                                          serials=template_set)
         return render( request, "home/WF1.html", context)
       else: # change type (4) is for a VC
         print("change type 3")
         swarm = request.POST.get('swarm_name').translate({ord('\''): None}).strip('][').split(', ')
         swarm_id = swarm[0]
         swarm_name = swarm[1]
         if (dev_type == 'IAP'):
            queryset = get_site_inventory(request,site, "AP")
            swarm_set = list()
            for each in queryset['aps']:
               if (swarm_id == each['swarm_id']):
                 swarm_set.append((each['serial'],each['name']))

         swarm_serial = swarm_set[0][0]
         queryset = get_variables(request, swarm_serial)
         if not queryset:  # no variables defined for the device
            messages.warning(request, 'No variables define for swarm '+ swarm_name)
            context = {'submit_button': "Next"}
            menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
            context['menu'] = menu
            context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
            return render( request, "home/WF1.html", context)
            
         variable_set = list()
         for each in queryset['data']['variables']:
             variable_set.append((each,each + ' (' + str(queryset['data']['variables'][each]) + ')'))

         context['submit_button'] = "Submit"
         context['form']= WF1SelectVariableVCForm(site_name=request.POST.get('site_name'),
                                          dev_type=request.POST.get('dev_type'),
                                          swarm_name = swarm_name,
                                          swarm_id = swarm_id,
                                          variables=variable_set,
                                          serials=swarm_set)
         return render( request, "home/WF1.html", context)




    elif (stage == '3'):
       print("STAGE 3 PROCESSING")
       dev_type = request.POST.get('dev_type')
       site = request.POST.get('site_name')
       template_name = request.POST.get('template_name')
       variable = request.POST.get('variable')
       value = request.POST.get('value')
       device_serial = request.POST.get('device_serial')
       override_commit_off = False
       if 'override_commit_off' in request.POST.keys():
          override_commit_off = True
       change_type = request.POST.get('change_type')
       
       if (change_type == "1"): #change type is for all devices in a template
         print("in change type 1")

         override_commit_off = False
         if 'override_commit_off' in request.POST.keys():
            override_commit_off = True
  
         if (dev_type == 'IAP'):
            queryset = get_site_inventory(request,site, "AP")
            dev_set = list()
            for each in queryset['aps']:
               if (template_name == each['group_name']):
                 dev_set.append((each['serial'],each['name']))
         else:
            queryset = get_site_inventory(request,site, "SWITCH")
            dev_set = list()
            for each in queryset['switches']:
               if (template_name == each['group_name']):
                 dev_set.append((each['serial'],each['name']))


         # here is where we set the variable for each of the serials in template_set
         for each in dev_set:

            if (override_commit_off):
               response = set_autocommit(request, "On", each[0])
               if response.status_code == 200:
                 messages.success(request, 'Commit set to ON for device ' + each[1] + ' (' + each[0] + ')')
               elif response.status_code == 400:
                 data = response.json()
                 messages.warning(request, 'FAILED - '+ data['description'])
               else:
                 data = response.json()
                 messages.warning(request, 'FAILED - '+ data['description']) 

            if "Success" in set_variable(request, each[0], variable, value ):
              messages.success(request, 'Variable ' + variable + ' updated to ' + value + ' in template ' + template_name + ' for device ' + each[1] + ' (' + each[0] + ')') 
            else:
              messages.warning(request, 'FAILED to set Variable = ' + variable + ' updated in template ' + template_name + ' for device ' + each[1] + ' (' + each[0] + ')') 



       elif (change_type == "2"): #change type is for a single device
         print("in change type 2")
         device_name = request.POST.get('device_name')

         if (override_commit_off):
            response = set_autocommit(request, "On", device_serial)
            if response.status_code == 200:
              messages.success(request, 'Commit set to ON for device ' + device_name + ' (' + device_serial + ')')
            elif response.status_code == 400:
              data = response.json()
              messages.warning(request, 'FAILED - '+ data['description'])
            else:
              data = response.json()
              messages.warning(request, 'FAILED - '+ data['description'])
         if "Success" in set_variable(request, device_serial, variable, value ):
           print(variable)
           print(value)
           print(device_name)
           print(device_serial)
           messages.success(request, 'Variable ' + variable + ' updated to ' + value + ' for device ' + device_name + ' (' + device_serial + ')')
         else:
           messages.warning(request, 'FAILED to set Variable = ' + variable + '  for device ' + device_name  + ' (' + device_serial + ')')

       elif (change_type == "3"): #change type is for a stack
         print("in change type 3")

         stack_name = request.POST.get('stack_name')
         stack_id = request.POST.get('stack_id')
         print(stack_name)
         print(stack_id)

         override_commit_off = False
         if 'override_commit_off' in request.POST.keys():
            override_commit_off = True

         if (dev_type == 'IAP'):
            queryset = get_site_inventory(request,site, "AP")
            dev_set = list()
            for each in queryset['aps']:
               if (stack_name == each['stack_name']):
                  dev_set.append((each['serial'],each['name']))
         else:
            queryset = get_site_inventory(request,site, "SWITCH")
            dev_set = list()
            for each in queryset['switches']:
               if (stack_id == each['stack_id']):
                  dev_set.append((each['serial'],each['name']))


         print(dev_set)

         # here is where we set the variable for each of the serials in template_set
         for each in dev_set:
            if (override_commit_off):
               response = set_autocommit(request, "On", each[0])
               if response.status_code == 200:
                 messages.success(request, 'Commit set to ON for device ' + each[1] + ' (' + each[0] + ')')
               elif response.status_code == 400:
                 data = response.json()
                 messages.warning(request, 'FAILED - '+ data['description'])
               else:
                 data = response.json()
                 messages.warning(request, 'FAILED - '+ data['description']) 

            if "Success" in set_variable(request, each[0], variable, value ):
              messages.success(request, 'Variable ' + variable + ' updated to ' + value + ' in stack: ' + stack_name + ' for device ' + each[1] + ' (' + each[0] + ')')
            else:
              messages.warning(request, 'FAILED to set Variable = ' + variable + ' updated in stack:  ' + stack_name + ' for device ' + each[1]  + ' (' + each[0] + ')')

       else:  #change type is for a VC
         print("in change type 4")

         swarm_name = request.POST.get('swarm_name')
         swarm_id = request.POST.get('swarm_id')
         print(swarm_name)
         print(swarm_id)

         override_commit_off = False
         if 'override_commit_off' in request.POST.keys():
            override_commit_off = True

         if (dev_type == 'IAP'):
            queryset = get_site_inventory(request,site, "AP")
            dev_set = list()
            for each in queryset['aps']:
               if (swarm_name == each['swarm_name']):
                  dev_set.append((each['serial'],each['name']))
         else:
            queryset = get_site_inventory(request,site, "SWITCH")
            dev_set = list()
            for each in queryset['switches']:
               if (swarn_id == each['swarm_id']):
                  dev_set.append((each['serial'],each['name']))


         # here is where we set the variable for each of the serials in template_set
         for each in dev_set:
            if (override_commit_off):
               response = set_autocommit(request, "On", each[0])
               if response.status_code == 200:
                 messages.success(request, 'Commit set to ON for device ' + each[1] + ' (' + each[0] + ')')
               elif response.status_code == 400:
                 data = response.json()
                 messages.warning(request, 'FAILED - '+ data['description'])
               else:
                 data = response.json()
                 messages.warning(request, 'FAILED - '+ data['description']) 

            if "Success" in set_variable(request, each[0], variable, value ):
              messages.success(request, 'Variable ' + variable + ' updated to ' + value + ' in swarm: ' + swarm_name + ' for device ' + each[1] + ' (' + each[0] + ')')
            else:
              messages.warning(request, 'FAILED to set Variable = ' + variable + ' updated in swarm:  ' + swarm_name + ' for device ' + each[1]  + ' (' + each[0] + ')')

       context = {'submit_button': "Next"}
       menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
       context['menu'] = menu
       context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
       return render( request, "home/WF1.html", context)

    elif (stage == '4'):
       print("STAGE 1 PROCESSING")
    else:
       print("NO STAGE PROCESSING")
       context = {'submit_button': "Next"}
       menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
       context['menu'] = menu
       context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
       return render( request, "home/WF1.html", context)

  else:
    context = {'submit_button': "Next"}
    menu = Menu.menu_objects.values('id','menu_name','group','menu_type','menu_url','menu_parent').order_by('menu_type')
    context['menu'] = menu
    context['form']= WF1SelectSiteForm(customer_id=request.user.profile.central_custID)
    return render( request, "home/WF1.html", context)


