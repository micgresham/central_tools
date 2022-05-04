# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views
#from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from .views import home, profile, RegisterView
from .common_views import test_central

#---------------------------------------------
# import your workflow functions here 
#---------------------------------------------
from .WFtg import create_tgroup, create_mtgroup, show_sites
from .WF1 import WF1select_site
from .WFcfg import WFcfg_select_site
from .WFsql import execute_sql



urlpatterns = [

    # The home page
    path('', views.home, name='home'),
 
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('test_central/', test_central, name='test_central'),

# Put your tasks here
    path('create_tgroup/', create_tgroup, name='create_tgroup'),
    path('create_mtgroup/', create_mtgroup, name='create_mtgroup'),
    path('show_sites/', show_sites, name='show_sites'),
    path('WF1select_site/', WF1select_site, name='WF1select_site'),
    path('WFcfg_select_site/', WFcfg_select_site, name='WFcfg_select_site'),
    path('WFsql/', execute_sql, name='sql'),


    # Matches any html file
    re_path(r'^.*\.htm', views.pages, name='pages'),
    re_path(r'^.*\.html', views.pages, name='pages')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

