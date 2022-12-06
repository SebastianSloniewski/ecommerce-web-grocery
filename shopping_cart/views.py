from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import View
import operator

from products.models import Product
from accounts.models import Order
from shopping_cart.models import Shopping_Cart, Cart_Item


class ShoppingCartSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            address = None
            if kwargs.get('id') is not None:
               id = kwargs.get('id')
               order = Order.objects.get(cart__user=self.request.user, cart__id=id)
               cart = order.cart
               address = order.address
            else:
               cart = Shopping_Cart.objects.get(user=self.request.user, ordered=False)

            context = {
                'object': cart,
                'address': address
            }
            return render(self.request, 'shopping-cart.html', context)
        except ObjectDoesNotExist:
            cart = Shopping_Cart.objects.create(user = self.request.user)
            messages.error(self.request, "Utworzono nowy koszyk", extra_tags="danger")
            return redirect("store:cart-summary")

        

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart_item, created = Cart_Item.objects.get_or_create(
        product=item,
        user=request.user,
        ordered=False
    )
    cart_qs = Shopping_Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        #check if the order product is already in the cart
        if cart.items.filter(product__slug = item.slug).exists():
            cart_item.quantity = cart_item.quantity + 1
            debugmessage = f"quantity: {cart_item.quantity}"
            messages.info(request, debugmessage)
            cart_item.save()
            messages.info(request, "Pomyślnie zwiększono ilość sztuk produktu.")
            return redirect("store:cart-summary")
        else:
            cart.items.add(cart_item)
            messages.info(request, "Produkt został dodany do koszyka.")
            return redirect("store:cart-summary")
    else:
        cart = Shopping_Cart.objects.create(user = request.user)
        cart.items.add(cart_item)
        messages.info(request, "nowy koszyk")
        return redirect("store:cart-summary")


@login_required
def remove_from_cart(request, slug):
    
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Shopping_Cart.objects.filter(user=request.user, ordered=False)
    
    if cart_qs.exists():
        cart = cart_qs[0]
        #check if the order product is already in the cart
        if cart.items.filter(product__slug = item.slug).exists():
            cart_item = Cart_Item.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            cart.items.remove(cart_item)
            cart_item.delete()
            messages.info(request, "Produkt został usunięty z twojego koszyka.")
            return redirect("store:cart-summary")

        else:
            messages.info(request, "Produkt nie znajdował się w twoim koszyku")
            return redirect("store:product-details",slug=slug)
        
    else:
        messages.info(request, "Nie posiadasz aktywnego koszyka.")
        return redirect("store:product-details",slug=slug)


@login_required
def remove_single_item(request,slug):
    item = get_object_or_404(Product, slug=slug)
    cart_qs = Shopping_Cart.objects.filter(
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
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart.items.remove(cart_item)
            messages.info(request, "Zaktualizowano")
            return redirect("store:cart-summary")
        else:
            messages.info(request, "Produkt nie znajfdował sie w koszyku")
            return redirect("store:product-details", slug=slug)
    else:
        messages.info(request, "Nie posiadasz aktywnego koszyka")
        return redirect("store:product-details", slug=slug)