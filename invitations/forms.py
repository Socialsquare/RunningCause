# coding: utf8
from django import forms


class EmailInviteForm(forms.Form):
    email = forms.EmailField(label="Friend's email address")
