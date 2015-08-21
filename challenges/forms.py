# coding: utf8

from datetime import date

from django import forms
from .models import Challenge


class ChallengeForm(forms.ModelForm):
    amount = forms.FloatField(label="Amount (kr)",
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}),
                              localize=True, required=True)
    end_date = forms.DateField(label="End date:",
                               widget=forms.DateInput(
                                    attrs={'class': 'form-control',
                                           'id': 'challenge_datepicker',
                                           'autocomplete': "off"}),
                               required=True)

    challenge_text = forms.CharField(label="What is the bet?",
                                     required=True,
                                     widget=forms.Textarea(
                                     attrs={'class': 'form-control'}))

    class Meta:
        model = Challenge
        fields = ['amount', 'end_date', 'challenge_text']

    def is_valid(self):

        valid = super(ChallengeForm, self).is_valid()

        if not valid:
            return valid

        if self.cleaned_data['amount'] < 0:
            self.add_error('amount', 'Amount cannot be negative')
            valid = False

        if self.cleaned_data['end_date'] < date.today():
            self.add_error('end_date', 'End date cannot be in the past')
            valid = False

        return valid


class ChallengeFeedbackForm(forms.Form):
    feedback_msg = forms.CharField(
        max_length=500, min_length=2,
        label="Please write a feedback message",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class ChallengeChallengePreviewForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['amount', 'end_date', 'challenge_text']

    def __init__(self, *args, **kwargs):
        super(ChallengeChallengePreviewForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for fname in self.fields:
                self.fields[fname].widget.attrs['readonly'] = True

