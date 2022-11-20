from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from .forms import CheckoutForm
from django.contrib import messages
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
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if  form.is_valid():
            print(form.cleaned_data)
            return redirect('store:checkout')
        return redirect('store:checkout')
       
            
