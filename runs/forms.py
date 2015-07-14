# coding: utf8

from django import forms

from .models import Run


class RunInputForm(forms.ModelForm):
    distance = forms.FloatField(label="Distance in km",
                                widget=forms.TextInput(),
                                localize=True)
    start_date = forms.DateField(label="Run date",
                                 widget=forms.DateInput(attrs={
                                     'id': 'start_datepicker',
                                     'autocomplete': "off"}))
    end_date = forms.DateField(label="End date",
                               widget=forms.DateInput(
                                   attrs={'id': 'end_datepicker',
                                          'autocomplete': "off"})
                               )
    recorded_time = forms.TimeField(label="Recorded time HH:MM:SS",
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
