from django import template
from products.models import *


register = template.Library()

@register.inclusion_tag('list_cate.html')
def show_categories(sort=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)


    return {'cats': cats}