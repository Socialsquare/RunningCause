# coding: utf8

from django import forms
from .models import Wager


class WagerForm(forms.ModelForm):
    amount = forms.FloatField(label="Amount:",
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}),
                              localize=True)
    remind_date = forms.DateField(label="End date:",
                                  widget=forms.DateInput(attrs={'class': 'form-control',
                                                                'id': 'wager_datepicker',
                                                                'autocomplete': "off"}),
                                  required=True)

    wager_text = forms.CharField(label="What is the bet?",
                                 widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Wager
        fields = ['amount', 'remind_date', 'wager_text']

    def is_valid(self):

        valid = super(WagerForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['amount'] < 0:
            self.add_error('amount', 'Amount cannot be negative')
            valid = False

        if self.cleaned_data['remind_date'] < date.today():
            self.add_error('remind_date', 'End date cannot be in the past')
            valid = False

        return valid


class WagerUpdateForm(forms.ModelForm):
    update_text = forms.CharField(label="What do you want to tell your sponsor?",
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Wager
        fields = ['update_text']


class InviteWagerForm(forms.Form):
    amount = forms.FloatField(label="Amount:",
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}),
                              localize=True,
                              required=False)
    remind_date = forms.DateField(label="End date:",
                                  widget=forms.DateInput(attrs={'class': 'form-control',
                                                                'id': 'wager_datepicker',
                                                                'autocomplete': "off"}),
                                  required=False)

    wager_text = forms.CharField(label="What is the bet?",
                                 widget=forms.Textarea(
                                     attrs={'class': 'form-control'}),
                                 required=False)

    def is_valid(self):

        valid = super(InviteWagerForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['amount'] and self.cleaned_data['amount'] < 0:
            self.add_error('amount', 'Amount cannot be negative')
            valid = False

        if self.cleaned_data['remind_date'] and self.cleaned_data['remind_date'] < date.today():
            self.add_error('remind_date', 'End date cannot be in the past')
            valid = False

        return valid
