from django import forms


class PaidForm(forms.Form):
    amount = forms.FloatField(label="Amount",
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}),
                              localize=True)
    sponsorship_id = forms.IntegerField(widget=forms.HiddenInput())
