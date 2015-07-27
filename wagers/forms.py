# coding: utf8

from datetime import date

from django import forms
from .models import Wager


class WagerForm(forms.ModelForm):
    amount = forms.FloatField(label="Amount:",
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}),
                              localize=True, required=True)
    end_date = forms.DateField(label="End date:",
                               widget=forms.DateInput(
                                    attrs={'class': 'form-control',
                                           'id': 'wager_datepicker',
                                           'autocomplete': "off"}),
                               required=True)

    wager_text = forms.CharField(label="What is the bet?",
                                 required=True,
                                 widget=forms.Textarea(
                                        attrs={'class': 'form-control'}))

    class Meta:
        model = Wager
        fields = ['amount', 'end_date', 'wager_text']

    def is_valid(self):

        valid = super(WagerForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['amount'] < 0:
            self.add_error('amount', 'Amount cannot be negative')
            valid = False

        if self.cleaned_data['end_date'] < date.today():
            self.add_error('end_date', 'End date cannot be in the past')
            valid = False

        return valid


class WagerFeedbackForm(forms.ModelForm):
    update_text = forms.CharField(label="What do you want to tell your sponsor?",
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Wager
        fields = ['update_text']


class WagerChallengePreviewForm(forms.ModelForm):
    class Meta:
        model = Wager
        fields = ['amount', 'end_date', 'wager_text']

    def __init__(self, *args, **kwargs):
        super(WagerChallengePreviewForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for fname in self.fields:
                self.fields[fname].widget.attrs['readonly'] = True

