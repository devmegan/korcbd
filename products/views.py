from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm

# Create your views here.


def products(request):
    """
    view returns products page and
    handles search/sorting queries
    """
    products = Product.objects.all()
    query_term = None
    category_name = None
    direction = None
    # handle blog searches by user
    if request.GET:
        if 'category' in request.GET:
            category_name = request.GET['category']
            if len(category_name) > 1:
                category_name = category_name.replace(",", " & ")
                print(category_name)
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)



        if 'search_q' in request.GET:
            query_term = request.GET['search_q']
            if not query_term:
                messages.error(request, "You didn't enter any search terms")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query_term) | Q(description__icontains=query_term) | Q(sku__icontains=query_term)
            products = products.filter(queries)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if 'direction' in request.GET:
                direction = request.GET['direction']
                print(direction)
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    context = {
        'products': products,
        'query_term': query_term,
        'category_name': category_name,
        'direction': direction,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, pk):
    """ view returns details product page """ 

    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ view for admin to add products to store """

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New product has been added to the store")
            return redirect('products')
        else:
            messages.error(request, 'Failed to add new product. Double check the form is valid.')
    else:
        form = ProductForm(request.POST)
    context = {
        'form': form
    }
    return render(request, 'products/add_product.html', context)