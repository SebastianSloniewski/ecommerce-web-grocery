
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.core.paginator import Paginator
from .models import Category, Product
from shopping_cart.models import *
from django.http import HttpResponse

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "shop-details.html"

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs['slug']).first()
        context={
            'product': product
        }
        response = HttpResponse(context)
        return render(request, self.template_name, context)



def basic_view(request):

    paginate_by = 16
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
            'categories': Category.objects.all(),
            'page_items': page_obj
        }

    return render(request, "shop-grid.html", context)


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
            cart_item.save()
            messages.info(request, "This item quantity was updated.")
        else:
            cart.items.add(cart_item)
            messages.info(request, "This item was added to your cart.")
        
        return redirect("store:product-details",slug=slug)
    else:
        cart = Shopping_Cart.objects.create(user = request.user)
        cart.items.add(cart_item)
        messages.info(request, "nowy koszyk")
        return redirect("store:product-details",slug=slug)



def remove_from_cart(request, slug):
    pass
#     item = get_object_or_404(Product, slug=slug)
#     cart_qs = Shopping_Cart.objects.filter(user=request.user, ordered=False)
#     if cart_qs.exists():
#         cart = cart_qs[0]
#         #check if the order product is already in the cart
#         if cart.items.filter(product__slug = item.slug).exists():
#             cart_item = Cart_Item.objects.filter(
#                 product=item,
#                 user=request.user,
#                 ordered=False
#             )[0]
#             cart.items.remove(cart_item)
#             messages.info(request, "This item quantity was updated.")
#         else:
#             cart.items.add(cart_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("store:product-details",slug=slug)
        
#     else:
#         cart = Shopping_Cart.objects.create(user = request.user)
#         cart.items.add(cart_item)
#         messages.info(request, "nowy koszyk")
#         return redirect("store:product-details",slug=slug)
