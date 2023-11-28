from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from users.models import User, Profile
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


class ForgotPasswordForm(forms.ModelForm):
    """ Форма відправки листа зміни пароля на пошту
    """
    email = forms.EmailField(max_length=120, widget=forms.EmailInput(
        attrs={'class': 'input-field col s12', 'placeholder': 'Пошта'}))

    class Meta:
        model = User
        fields = ('email',)


class SetPasswordForm(forms.Form):
    """ Форма встановлення нового пароля
    """
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input-field col s12', 'placeholder': 'Пароль'}), strip=False)
    re_new_password = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'class': 'input-field col s12', 'placeholder': 'Повтор пароля'}))

    def error_400(self, error):
        data = json.loads(error)
        error_pass = data.get('new_password')
        error_detail = data.get('non_field_errors')
        error_token = data.get('token')
        if error_pass:
            self.add_error('new_password', error_pass)
        if error_token:
            self.add_error('new_password', 'Час зміни пароля минув')
        if error_detail:
            self.add_error('re_new_password', 'Паролі на збігаються')

    class Meta:
        model = User
        fields = ('password1', 'password2')


class ProfileForm(forms.ModelForm):
    """Форма збереження контактних даних юзера у профілю
    """
    phone_number = forms.CharField(label='Номер телефону:', widget=PhoneNumberPrefixWidget(
        attrs={'type': 'text', 'name': 'phone_number', 'maxlength': '14'}))
    adress = forms.CharField(
        label='12', help_text='Для коректного збереження цього поля, використовуйте такий формат:\n" Вулиця номер_будинку номер_квартири "\nНаприклад:\nЗакревського 155 50')

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'surname',
                  'phone_number', 'department', 'city', 'adress')
