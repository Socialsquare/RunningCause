# coding: utf8
from django import forms
from django.utils.translation import ugettext as _

class EmailInviteForm(forms.Form):
    email = forms.EmailField(label=_("Friend's email address"))
