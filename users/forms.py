from django.contrib.auth.forms import AuthenticationForm
from django import forms
from users.models import User
import json


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    re_password = forms.CharField(
        label='Повторний пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def clean_password2(self):
        cd = self.data
        if cd['password'] != cd['re_password']:
            self.add_error('re_password', 'Паролі не збігаються')
        return cd['re_password']

    def error_400(self, error):
        data = json.loads(error)
        error_pass = data.get('password')
        error_detail = data.get('details')
        if error_pass:
            self.add_error('password', error_pass)
        if error_detail:
            self.add_error('email', error_detail)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Пошта / Логін')
