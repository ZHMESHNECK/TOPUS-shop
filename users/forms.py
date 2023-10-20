from django.contrib.auth.forms import AuthenticationForm
from django import forms
from users.models import User
import json


class UserRegistrationForm(forms.ModelForm):
    """Форма реєстрації
    """
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'class': 'input', 'placeholder': 'Пошта'}))
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Логін'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': 'Пароль'}))
    re_password = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Повторний пароль'}))

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
    """ Форма логіну
    """

    username = forms.CharField(
        label='Пошта / Логін')
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput)


class ForgotPasswordForm(forms.ModelForm):
    """ Форма відправки листа зміни пароля на пошту
    """
    email = forms.EmailField(label='Пошта')

    class Meta:
        model = User
        fields = ('email',)


class SetPasswordForm(forms.Form):
    """ Форма встановлення нового пароля
    """
    new_password = forms.CharField(label='Новий пароль',
                                   widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), strip=False)
    re_new_password = forms.CharField(label='Повтор нового пароля', strip=False,
                                      widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    def error_400(self, error):
        data = json.loads(error)
        error_pass = data.get('new_password')
        error_detail = data.get('details')
        if error_pass:
            self.add_error('new_password', error_pass)
        if error_detail:
            self.add_error('new_password', error_detail)

    class Meta:
        model = User
        fields = ('password1', 'password2')
