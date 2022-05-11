# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from django.urls import re_path as url
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView

#urlpatterns = [
#    path('login/', login_view, name="login"),
#    path('register/', register_user, name="register"),
#    path("logout/", LogoutView.as_view(), name="logout")
#]

from django.contrib.auth import views as auth_views
from apps.home.views import CustomLoginView, ResetPasswordView, ChangePasswordView

from apps.home.forms import LoginForm

urlpatterns = [
#    path('admin/', admin.site.urls),

#    path('', include('apps.home.urls')),

    path('register/', register_user, name="register"),
    path('login/', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
#    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='home/login.html',
#                                           authentication_form=LoginForm), name='login'),

#    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),

    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),
         name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

#    url(r'^oauth/', include('social_django.urls', namespace='social')),

] 
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
