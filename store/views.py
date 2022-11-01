from django.shortcuts import render

from products.models import *

# Create your views here.
def index_view(request):
    context = {
            'categories': Category.objects.all(),
        }

    return render(request, "index.html", context)