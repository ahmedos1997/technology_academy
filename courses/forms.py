from django import forms
from . import models
from django.utils.translation import gettext as _



# comment

attrs = {'class': 'form-control'}







class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['title']
        labels = {
            'title': _('title'),
        }
        widgets = {
            'title': forms.TextInput(),
        }



# Replie


class ReplieCreateForm(forms.ModelForm):
    class Meta:
        model = models.Replie
        fields = ['title']
        labels = {
            'title': _('title'),
        }
        widgets = {
            'title': forms.TextInput(),
        }


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = models.Subscriber
        fields = ['name']
        labels = {
            'name': _('name'),
        }
        widgets = {
            'name': forms.TextInput(attrs=attrs),
        }