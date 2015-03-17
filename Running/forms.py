from django import forms
from Running.models import Sponsorship, Run, Wager
from django.contrib.admin import widgets
from functools import partial
from datetime import date

DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class SponsorForm(forms.ModelForm):
    rate = forms.FloatField(label="Rate", 
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            localize=True)
    start_date = forms.DateField(label="Sponsorship start date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'start_datepicker', 
                                                                        'autocomplete':"off"}),
                                required=True)
    end_date = forms.DateField(label="Sponsorship end date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'end_datepicker', 
                                                                        'autocomplete':"off"}),
                                required=True)
    max_amount = forms.FloatField(label="Maximum total amount", 
                                    widget=forms.TextInput(attrs={'class':'form-control'}), 
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

class WagerForm(forms.ModelForm):
    amount = forms.FloatField(label="Amount:", 
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            localize=True)
    remind_date = forms.DateField(label="End date:", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'wager_datepicker', 
                                                                        'autocomplete':"off"}),
                                required=True)

    wager_text = forms.CharField(label="What is the bet?", 
                                    widget=forms.Textarea(attrs={'class':'form-control'}))

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
                                    widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Wager
        fields = ['update_text']

class InviteWagerForm(forms.Form):
    amount = forms.FloatField(label="Amount:", 
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            localize=True,
                            required=False)
    remind_date = forms.DateField(label="End date:", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'wager_datepicker', 
                                                                        'autocomplete':"off"}),
                                required=False)

    wager_text = forms.CharField(label="What is the bet?", 
                                    widget=forms.Textarea(attrs={'class':'form-control'}),
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

class PaidForm(forms.Form):
    amount = forms.FloatField(label="Amount",
                                widget=forms.TextInput(attrs={'class':'form-control'}),
                                localize=True)
    sponsorship_id = forms.IntegerField(widget=forms.HiddenInput())

class InviteForm(forms.Form):
    rate = forms.FloatField(label="Rate", 
                            widget=forms.TextInput(attrs={'class':'form-control'}),
                            required=False,
                            localize=True)
    start_date = forms.DateField(label="Sponsorship start date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'start_datepicker', 
                                                                        'autocomplete':"off"}),
                                required=False)
    end_date = forms.DateField(label="Sponsorship end date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                                        'id':'end_datepicker', 
                                                                        'autocomplete':"off"}),
                                required=False)
    max_amount = forms.IntegerField(label="Maximum total amount", 
                                    widget=forms.TextInput(attrs={'class':'form-control'}),
                                    required=False,
                                    localize=True)

    def is_valid(self):
 
        valid = super(InviteForm, self).is_valid()
 
        if not valid:
            return valid
 
        if self.cleaned_data['rate'] < 0 and self.cleaned_data['rate'] != None:
            self.add_error('rate', 'Rate cannot be negative')
            valid = False
            
        if self.cleaned_data['max_amount'] < 0 and self.cleaned_data['max_amount'] != None:
            self.add_error('max_amount', 'Max amount cannot be negative')
            valid = False


        if self.cleaned_data['start_date'] != None and self.cleaned_data['end_date'] != None and self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
            self.add_error('end_date', 'End date cannot be before start date.')
            valid = False

        return valid

class EmailInviteForm(InviteForm):
    email = forms.EmailField(label="Potential Sponsor's email account:",
                                widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(EmailInviteForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['rate', 'start_date', 'end_date', 'max_amount', 'email']

class SignupForm(forms.Form):
    public_info = forms.BooleanField(label="Do you want your sponsorships to be publicly visible?", 
                                        widget=forms.CheckboxInput(),
                                        required=False)

    newsletter = forms.BooleanField(label="Would you like to recieve the Masanga newsletter?",
                                        widget=forms.CheckboxInput(),
                                        required=False)

    def signup(self, request, user):
        user.is_public = self.cleaned_data['public_info']
        user.newsletter = self.cleaned_data['newsletter']
        user.save()

class RunInputForm(forms.ModelForm):
    distance = forms.FloatField(label="Distance in km", 
                                widget=forms.TextInput(attrs={'class':'form-control'}),
                                localize=True)
    start_date = forms.DateField(label="Run date", 
                                    widget=forms.DateInput(attrs={'class':'form-control', 
                                                                    'id':'start_datepicker', 
                                                                    'autocomplete':"off"}))
    end_date = forms.DateField(label="End date", 
                                widget=forms.DateInput(attrs={'class':'form-control', 
                                                            'id':'end_datepicker', 
                                                            'autocomplete':"off"}), 
                                required=False)


    class Meta:
        model = Run
        fields = ['distance', 'start_date', 'end_date']

    def is_valid(self):
 
        valid = super(RunInputForm, self).is_valid()
 
        if not valid:
            return valid
 
        if self.cleaned_data['distance'] < 0:
            self.add_error('distance', 'Distance cannot be negative')
            valid = False

        return valid