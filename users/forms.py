from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.translation import gettext as _



from . import models

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

attrs = {'class': 'form-control'}


class UserLogin(AuthenticationForm):
    def __int__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label= _('Username'),
        widget=forms.TextInput(attrs=attrs),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs=attrs)
    )


class Register(UserCreationForm):
    first_name = forms.CharField(
        label=_('First Name'),
        widget=forms.TextInput(attrs=attrs),
    )
    last_name = forms.CharField(
        label=_('last Name'),
        widget=forms.TextInput(attrs=attrs),
    )
    username = forms.CharField(
        label=_('User name'),
        widget=forms.TextInput(attrs=attrs)
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(attrs=attrs),
    )
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs),
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs),
    )

    class Meta(UserCreationForm.Meta):  # تعريف الحقول المطلوبة باستخدام meta
        fields = ('first_name', 'last_name', 'username', 'email')

class Profile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': _('first_name'),
            'last_name': _('last_name'),
            'email': _('email')
        }
        widgets = {
            'first_name' : forms.TextInput(attrs=attrs),
            'last_name': forms.TextInput(attrs=attrs),
            'email': forms.EmailInput(attrs=attrs),
        }

