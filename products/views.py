from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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

def search_products(request):
    query_term = None
    products = Product.objects.all()

    # handle blog searches by user
    if request.GET:
        if 'search_q' in request.GET:
            query_term = request.GET['search_q']
            if not query_term:
                messages.error(request, "You didn't enter any search terms")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query_term) | Q(description__icontains=query_term) | Q(sku__icontains=query_term)
            query_products = products.filter(queries)
        context = {
            'products': query_products,
            'query_term': query_term,
        }
        return render(request, 'products/products.html', context)

def product_detail(request, pk):
    """
    view returns details product page
    """

    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)