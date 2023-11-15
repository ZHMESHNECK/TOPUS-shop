from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from users.models import Profile


class PhoneNumber(forms.ModelForm):
    phone_number = forms.CharField(label='', widget=PhoneNumberPrefixWidget(attrs={'type':'text','name':'phone_number','maxlength':'14'}))

    
    class Meta:
        model = Profile
        fields = ('phone_number',)