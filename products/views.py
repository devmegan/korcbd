from django.shortcuts import render
from .models import Product

# Create your views here.


def products(request):
    """
    view returns products page and
    handles search/sorting queries
    """

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)