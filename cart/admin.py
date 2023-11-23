from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from cart.models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'product_info', 'quantity', 'city',
                    'ordered_date', 'is_pay', 'status')
    readonly_fields = ('customer', 'product', 'city',
                       'quantity', 'ordered_date')
    list_filter = ('ordered_date', 'status')
    list_editable = ('status',)
    search_fields = ('product', 'customer')

    def customer_info(self, obj):
        link = reverse('admin:users_customer_change', args=[obj.customer_id])
        return format_html(f'<a href="{link}">{obj.customer.last_name}</a>')
    customer_info.short_description = 'Замовник'

    def product_info(self, obj): 
        if obj.product.category.slug == 'cloth':
            product = 'clothes'
        elif obj.product.category.slug == 'for_home':
            product = 'home'
        else:
            product = obj.product.category.slug
        link = reverse(
            f'admin:products_{product}_change', args=(obj.product_id,))
        return format_html(f'<a href="{link}">{obj.product.title} - {obj.product.brand}</a>')
    product_info.short_description = 'Товар'
