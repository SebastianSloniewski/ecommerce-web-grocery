
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Category, Product
from shopping_cart.models import *
from django.http import HttpResponse
import operator

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "shop-details.html"


    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs['slug']).first()
        product_category_id = product.category.id
        category_items = Product.objects.filter(category__id=product_category_id).exclude(id=product.id)
        context={
            'product': product,
            'items': category_items
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

