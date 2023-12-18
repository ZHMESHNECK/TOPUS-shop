from django import template
from products.models import Category, MainModel
from cart.models import Cart

register = template.Library()


@register.inclusion_tag('list_cate.html')
def show_categories(sort=None):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats}


@register.simple_tag()
def show_count_cart(request):
    return Cart(request).__len__()

@register.simple_tag()
def pagination_range(number):
    return list(range(number))


@register.simple_tag()
def len_history(request):
    return len(request.session.get('viewed_products', []))


@register.simple_tag()
def len_favourite(request):
    if not request.user.is_anonymous:
        return len(MainModel.objects.filter(is_published=True, in_liked=request.user.id).only('id'))
    else:
        return len(request.session.get('favourite_products', []))
