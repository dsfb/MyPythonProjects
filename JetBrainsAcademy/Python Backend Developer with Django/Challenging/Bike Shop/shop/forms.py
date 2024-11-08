
from django import forms


class BikeOrderingForm(forms.Form):
    name = forms.CharField(label='your name:')
    surname = forms.CharField(label='your surname:')
    phone_number = forms.CharField(label='your phone number:')