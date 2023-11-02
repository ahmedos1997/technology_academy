from django import forms
from . import models
from django.utils.translation import gettext as _


class BlogCreateForm(forms.ModelForm):
    class Meta:

        model = models.Blog
        fields = ['title','body']
        labels = {
            'title': _('title'),
            'body': _('body')
        }
        widgets = {
            'title': forms.TextInput(),
            'body': forms.Textarea(),
        }



class BlogUpdateForm(forms.ModelForm):
    class Meta:

        model = models.Blog
        fields = ['title','body']
        labels = {
            'title': _('title'),
            'body': _('body')
        }
        widgets = {
            'title': forms.TextInput(),
            'body': forms.Textarea(),
        }