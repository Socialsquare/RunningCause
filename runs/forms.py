# coding: utf8

from django import forms
from django.utils.translation import ugettext as _

from .models import Run


class RunInputForm(forms.ModelForm):
    distance = forms.FloatField(label=_("Distance (km)"),
                                widget=forms.TextInput(),
                                localize=True)
    start_date = forms.DateField(label=_("Run date"),
                                 widget=forms.DateInput(attrs={
                                     'id': 'start_datepicker',
                                     'autocomplete': "off"}))
    end_date = forms.DateField(label=_("End date (if entering multiple runs)"),
                               required=False,
                               widget=forms.DateInput(
                                   attrs={'id': 'end_datepicker',
                                          'autocomplete': "off"})
                               )
    recorded_time = forms.DurationField(label=_("Time (HH:MM:SS, optional)"),
                                        required=False)

    class Meta:
        model = Run
        fields = ['distance', 'start_date', 'end_date', 'recorded_time']

    def is_valid(self):

        valid = super(RunInputForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['distance'] < 0:
            self.add_error('distance', 'Distance cannot be negative')
            valid = False

        return valid
