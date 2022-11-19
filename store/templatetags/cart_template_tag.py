
from django import template
from shopping_cart.models import Shopping_Cart as cart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = cart.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0  

@register.filter
def get_cart(user):
    if user.is_authenticated:
        c = cart.objects.filter(user=user, ordered=False)[0]
        total = 0
        for cart_item in c.items.all():
            total += cart_item.product.price
        return total
    return 0