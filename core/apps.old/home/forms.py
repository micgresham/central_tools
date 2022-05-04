## accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from .models import Profile, CentralSites

class PlainTextWidgetWithHiddenCopy(forms.Widget):
    def render(self, name, value, attrs, renderer=None):
        if hasattr(self, 'initial'):
            value = self.initial

        return mark_safe(
            '<b>' + (str(value) if value is not None else '-') +
            f"</b><input type='hidden' name='{name}' value='{value}'><br>"
        )

class UpdateUserForm(ModelForm):
     class Meta:
       model = User
       fields = (
            'email',
            'first_name',
            'last_name',
           )

class UpdateProfileForm(ModelForm):
# fields we want to include and customize in our form

    class Meta:

       model = Profile
       fields = (
          'avatar',
          'central_url',
          'central_custID',
          'central_clientID',
          'central_client_secret',
          'central_token',
          'central_refresh_token',
          'central_tokenID'
       )


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    central_username = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Central Username',
                                                             'class': 'form-control',
                                                             }))
    central_password = forms.CharField(max_length=50,
                                required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Central Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'central_password',
                                                                  }))
    central_url = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.URLInput(attrs={'class': 'form-control',
                                                             }))
    central_custID = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             }))
    central_clientID = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             }))
    central_client_secret = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             }))
    central_token = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             }))
    central_refresh_token = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             }))
    central_tokenID = forms.CharField(max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             }))

    class Meta:
        model = Profile
        fields = ['avatar', 'central_url','central_username','central_password','central_custID','central_clientID','central_client_secret','central_token','central_refresh_token','central_tokenID']

