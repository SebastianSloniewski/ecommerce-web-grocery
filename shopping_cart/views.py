from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from products.models import Product

from shopping_cart.models import Shopping_Cart, Cart_Item


class ShoppingCartSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            cart = Shopping_Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': cart
            }
            return render(self.request, 'shopping-cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "Nie masz aktywnego koszyka")
            return redirect("/")
        
@login_required
def remove_single_item(request,slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Shopping_Cart.objects.filter(
        product=item,
        user=request.user,
        ordered=False
    )
    if cart_qs.exists():
        cart = cart_qs[0]
        if cart.items.filter(product__slug=item.slug).exists():
            cart_item = Cart_Item.objects.filter(
                product = item,
                user = request.user,
                ordered = False
            )[0]
            cart_item.quantity -= 1
            cart_item.save()
            messages.info(request, "This item was updated")
            return redirect("store:cart-summary", slug=slug)

