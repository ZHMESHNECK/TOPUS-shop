from django.contrib import admin
from users.models import *


@admin.register(Profile)
class UserProfileUAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
