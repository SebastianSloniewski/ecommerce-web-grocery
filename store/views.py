from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from .forms import CheckoutForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from accounts.models import Address
from products.models import *
from shopping_cart.models import *


# Create your views here.
def index_view(request):
    context = {
            'categories': Category.objects.all(),
        }

    return render(request, "index.html", context)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        cart = Shopping_Cart.objects.get(user=self.request.user, ordered=False)
        total_price = cart.get_total_price()
        total_items = cart.items_count()
        context = {
            'form': form,
            'total_price': total_price,
            'items_count': total_items
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            cart = Shopping_Cart.objects.get(user=self.request.user, ordered = False)
            if  form.is_valid():
                name = form.cleaned_data.get("name")
                surname = form.cleaned_data.get("surname")
                street_address = form.cleaned_data.get("street_address")
                building_address = form.cleaned_data.get("building_address")
                apartment_address = form.cleaned_data.get("apartment_address")
                city = form.cleaned_data.get("city")
                postal_code = form.cleaned_data.get("postal_code")
                phone_number = form.cleaned_data.get("phone_number")
                email = form.cleaned_data.get("email")
                address = Address(
                    user = self.request.user,
                    street_address = street_address,
                    building_address = building_address,
                    apartment_address = apartment_address,
                    city = city,
                    postal_code = postal_code
                )
                address.save()
                return redirect('store:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "Nie posiadasz aktywnego zamówienia")
            return redirect("store:cart-summary")
        
        return redirect('store:checkout')
       
            
