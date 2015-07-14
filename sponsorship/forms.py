# coding: utf8
from django import forms

from .models import Sponsorship, SponsorRequest


class SponsorForm(forms.ModelForm):
    rate = forms.FloatField(label="Rate",
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}),
                            localize=True)
    start_date = forms.DateField(label="Sponsorship start date",
                                 widget=forms.DateInput(attrs={'class': 'form-control',
                                                               'id': 'start_datepicker',
                                                                        'autocomplete': "off"}),
                                 required=True)
    end_date = forms.DateField(label="Sponsorship end date",
                               widget=forms.DateInput(attrs={'class': 'form-control',
                                                             'id': 'end_datepicker',
                                                             'autocomplete': "off"}),
                               required=True)
    max_amount = forms.FloatField(label="Maximum total amount",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control'}),
                                  localize=True)

    class Meta:
        model = Sponsorship
        fields = ['rate', 'start_date', 'end_date', 'max_amount']

    def is_valid(self):

        valid = super(SponsorForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['rate'] < 0:
            self.add_error('rate', 'Rate cannot be negative')
            valid = False

        if self.cleaned_data['max_amount'] < 0:
            self.add_error('max_amount', 'Max amount cannot be negative')
            valid = False

        if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
            self.add_error('end_date', 'End date cannot be before start date.')
            valid = False

        return valid
