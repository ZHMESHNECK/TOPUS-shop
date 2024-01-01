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
    list_display = ('user', 'beautiful_number')
    fields = ('user', 'first_name', 'last_name', 'surname',
              'phone_number', 'department', 'city', 'adress')
    readonly_fields = ('user',)

    def beautiful_number(self, obj):
        if not isinstance(obj.phone_number, str):
            return obj.phone_number.as_international
        return '-'

    beautiful_number.short_description = 'Телефон'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('email', 'username')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'first_name', 'last_name',
                    'surname', 'beautiful_number', 'email')
    readonly_fields = ('profile', 'first_name', 'last_name',
                       'surname', 'phone_number', 'email')
    search_fields = ('phone_number', 'email')
    list_select_related = ('profile',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

    def beautiful_number(self, obj):
        if obj.phone_number.national_number:
            return obj.phone_number.as_international
        return '-'

    beautiful_number.short_description = 'Телефон'
