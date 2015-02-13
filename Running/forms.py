from django import forms
from Running.models import Sponsorship
from django.contrib.admin import widgets
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class SponsorForm(forms.ModelForm):
    rate = forms.FloatField(label="Rate", 
                            widget=forms.TextInput(attrs={'class':'form-control'}))
    end_date = forms.DateField(label="Sponsorship end date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'datepicker', 
                                                                        'autocomplete':"off"}),
                                required=False)
    max_amount = forms.IntegerField(label="Maximum total amount", widget=forms.TextInput(attrs={'class':'form-control'}))
    single_day = forms.BooleanField(label="Should this sponsorship be for a single day? (The end date will also be the start date)",
                                    widget=forms.CheckboxInput(),
                                    required=False)
    class Meta:
        model = Sponsorship
        fields = ['rate', 'end_date', 'max_amount', 'single_day']

class PaidForm(forms.Form):
    amount = forms.FloatField(label="Amount",
                                widget=forms.TextInput(attrs={'class':'form-control'}))
    sponsorship_id = forms.IntegerField(widget=forms.HiddenInput())

class InviteForm(forms.Form):
    rate = forms.FloatField(label="Rate", 
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=False)
    end_date = forms.DateField(label="Sponsorship end date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'datepicker', 
                                                                        'autocomplete':"off"}),
                                required=False)
    max_amount = forms.IntegerField(label="Maximum total amount", 
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    required=False)
    single_day = forms.BooleanField(label="Should this sponsorship be for a single day? (The end date will also be the start date)",
                                    widget=forms.CheckboxInput(),
                                    required=False)

class SignupForm(forms.Form):
    public_info = forms.BooleanField(label="Do you want your sponsorships to be publicly visible?", 
                                        widget=forms.CheckboxInput(),
                                        required=False)
    # email = forms.EmailField(label="Your email")

    def signup(self, request, user):
        user.is_public = self.cleaned_data['public_info']
        # user.last_name = self.cleaned_data['last_name']
        user.save()

class RunInputForm(forms.Form):
    distance = forms.FloatField(label="Distance in km", widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateField(label="Run date", 
                            widget=forms.DateInput(attrs={'class':'form-control', 
                                                            'id':'start_datepicker', 
                                                            'autocomplete':"off"}))
    end_date = forms.DateField(label="End date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                            'id':'end_datepicker', 
                                                            'autocomplete':"off"}), 
                                required=False)