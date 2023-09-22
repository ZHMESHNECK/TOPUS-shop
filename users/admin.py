from django import forms
from django.contrib import admin
from users.models import *

from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ProfileFormAdmin(forms.ModelForm):
    class Meta:
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(),
        }


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    form = ProfileFormAdmin
    fields = ('user', 'phone_number', 'department')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('email', 'username')
