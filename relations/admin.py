from relations.models import Relation
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Relation)
class RatingAdmin(admin.ModelAdmin):
    fields = ('user', 'product_info', 'rate', 'comment', 'parent')
    list_select_related = ('user', 'parent', 'item')
    readonly_fields = ('user', 'product_info', 'parent')
    ordering = ('-id',)

    def save_model(self, request, obj, form, change):
        Relation.objects.update_or_create(
            user=obj.user, item=obj.item, defaults={
                'rate': obj.rate, 'comment': obj.comment, 'parent': obj.parent}
        )

    def product_info(self, obj):
        list_products = []
        obj = Relation.objects.select_related('user').prefetch_related('item__category').get(id=obj.id)
        product = obj.item

        if product.category.slug == 'cloth':
            product = 'clothes'
        elif product.category.slug == 'for_home':
            product = 'home'
        else:
            product = product.category.slug

        link = reverse(
            f'admin:products_{product}_change', args=(obj.item_id,))

        list_products.append(format_html(
            f'<a href="{link}">{obj.item.title} - {obj.item.brand}</a>'))
        
        return format_html('<br>'.join(list_products))
    
    product_info.short_description = 'Товар'
