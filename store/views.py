from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import operator
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .forms import CheckoutForm
from .models import *

# Create your views here.
def index_view(request):
    context = {
            'categories': Category.objects.all(),
            'featured' : Product.objects.filter(featured=True)
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
        if total_items == 0:
            messages.error(self.request, "Twój koszyk jest pusty")
            return redirect("store:cart-summary")
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

                cart.ordered = True
                cart.save()

                order = Order(
                    address = address, 
                    phone = phone_number,
                    email = email,
                    cart = cart,
                    order_date = timezone.now())
                order.save()
                
                return redirect('store:orders-history')
        except ObjectDoesNotExist:
            messages.error(self.request, "Nie posiadasz aktywnego zamówienia")
            return redirect("store:cart-summary")
        
        return redirect('store:checkout')
       

class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        orders = Order.objects.all().filter(cart__user = self.request.user)

        context = {
            'orders': orders,
            'categories': Category.objects.all(),
        }
        return render(self.request, "orders.html", context)


class ShoppingCartSummaryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        try:
            cart = Shopping_Cart.objects.get(user=self.request.user, ordered=False)

            context = {
                'object': cart
            }
            return render(self.request, 'shopping-cart.html', context)

        except ObjectDoesNotExist:
            cart = Shopping_Cart.objects.create(user = self.request.user)
            messages.info(self.request, "Utworzono nowy koszyk", extra_tags="danger")
            return redirect("store:cart-summary")

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        id = kwargs.get('id')
        order = Order.objects.get(cart__user=self.request.user, cart__id=id)
        cart = order.cart
        address = order.address
        context = {
            'object': cart,
            'address': address
        }
        return render(self.request, 'shopping-cart.html', context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    cart_item, created = Cart_Item.objects.get_or_create(
        product=item,
        ordered=False
    )
    cart_qs = Shopping_Cart.objects.filter(user=request.user, ordered=False)
    if cart_qs.exists():
        cart = cart_qs[0]
        #check if the order product is already in the cart
        if cart.items.filter(product__slug = item.slug).exists():
            cart_item.quantity = cart_item.quantity + 1
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


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "shop-details.html"


    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs['slug']).first()
        product_category_id = product.category.id
        category_items = Product.objects.filter(category__id=product_category_id).exclude(id=product.id)
        categories = Category.objects.all()
        context={
            'product': product,
            'items': category_items,
            'categories' : categories
        }
        response = HttpResponse(context)
        return render(request, self.template_name, context)



def shop_view(request):

    paginate_by = 15
    products = Product.objects.all()

    data = {
        'category':request.GET.get('category'),
        'page_number': request.GET.get('page') 
    }
    data = {k: v for k, v in data.items() if v}
    print(data)
    if "category" in data:
        products = Product.objects.filter(category_id=data['category'])

    paginator = Paginator(products, paginate_by)
    page_obj = paginator.get_page(1)
    
    if "page_number" in data:
        page_obj = paginator.get_page(data['page_number'])
    
    
    context = {
            'products': products,
            'categories': sorted(Category.objects.all(), key=operator.attrgetter('category_name')),
            'page_items': page_obj,
            'discount_items': products.filter(discount__gt=0)
        }

    return render(request, "shop-grid.html", context)
