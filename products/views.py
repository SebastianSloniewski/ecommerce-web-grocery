
from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Category, Product



# Create your views here.
def product_list(request, category=None):
    if category is None:
        context = {
            'items': Product.objects.all(),
            'categories': Category.objects.all()
        }
    else:
        context = {
            'items': Product.objects.filter(category_name=category),
            'categories': Category.objects.all()
        }
    return render(request, "shop-grid.html", context)

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
