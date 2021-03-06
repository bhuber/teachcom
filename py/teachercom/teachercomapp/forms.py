from django import forms
from registration.forms import RegistrationForm

import models
from registration.models import RegistrationProfile

attrs_dict = { 'class': 'required' }

class UserRegistrationForm(RegistrationForm):
    twilio_account_sid = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    twilio_auth_token = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    twilio_number = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
