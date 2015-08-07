# coding: utf8

from django import forms


class SignupForm(forms.Form):
    public_info = forms.BooleanField(label="I want my sponsorships to be publicly visible",
                                     widget=forms.CheckboxInput(),
                                     required=False,
                                     initial=True)

    newsletter = forms.BooleanField(label="I would like to recieve the Masanga newsletter",
                                    widget=forms.CheckboxInput(),
                                    required=False,
                                    initial=True)

    def signup(self, request, user):
        user.is_public = self.cleaned_data['public_info']
        user.newsletter = self.cleaned_data['newsletter']
        user.save()
