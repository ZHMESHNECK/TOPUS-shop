from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Prefetch
from cart.models import Order, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_info', 'city',
                    'ordered_date', 'is_pay', 'status')
    readonly_fields = ('customer', 'product_info', 'city',
                       'ordered_date', 'beauty_number')
    list_filter = ('ordered_date', 'status')
    list_editable = ('status',)
    list_select_related = ('customer',)
    search_fields = ('product', 'customer')
    exclude = ('summ_of_pay',)

    def customer_info(self, obj):
        link = reverse('admin:users_customer_change', args=[obj.customer_id])
        return format_html(f'<a href="{link}">{obj.customer.last_name}</a>')
    customer_info.short_description = 'Замовник'

    def product_info(self, obj):
        list_products = []
        products = obj.orderproduct_set.select_related('product__category')

        for num, order_product in enumerate(products, 1):
            quantity = order_product.quantity
            item = order_product.product

            if item.category.slug == 'cloth':
                product = 'clothes'
            elif item.category.slug == 'for_home':
                product = 'home'
            else:
                product = item.category.slug

            link = reverse(
                f'admin:products_{product}_change', args=(item.id,))

            list_products.append(format_html(
                f'{num}) <a href="{link}">{item.title} - {item.brand}</a>, {quantity} шт.'))
        return format_html('<br>'.join(list_products))
    product_info.short_description = 'Товар'

    def beauty_number(self, obj):
        return f'{obj.summ_of_pay:,.2f} грн'
    beauty_number.short_description = 'Всього'
