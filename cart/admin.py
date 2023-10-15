from django.contrib import admin

from cart.models import *

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass

