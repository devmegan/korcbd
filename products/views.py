from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm

# Create your views here.


def products(request):
    """
    view returns products page and
    handles search/sorting queries
    """
    products = Product.objects.all().order_by("price")
    # products = products.order_by("price")
    query_term = None
    category_name = None
    direction = None
    # handle blog searches by user
    if request.GET:
        if 'category' in request.GET:
            category_name = request.GET['category']
            if len(category_name) > 1:
                category_name = category_name.replace(",", " & ")
            categories = request.GET['category'].split(',')
            categories = categories
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'search_q' in request.GET:
            query_term = request.GET['search_q']
            if not query_term:
                messages.error(request, "You didn't enter any search terms")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query_term) | \
                Q(description__icontains=query_term) | \
                Q(ingredients__icontains=query_term) | \
                Q(sku__icontains=query_term)

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
    qty_in_cart = 0
    cart = request.session.get('cart', {})
    for product_id, quantity in cart.items():
        if int(product_id) == int(pk):
            qty_in_cart = quantity
    context = {
        'product': product,
        'qty_in_cart': qty_in_cart,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ view for admin to add products to store """
    # only allow super user access
    if not request.user.is_superuser:
        messages.error(
            request,
            "You must be logged in as KOR admin to do this"
        )
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            messages.info(
                request,
                f"New product, {new_product.name} has been added to the store"
            )
            return redirect(reverse('product_detail', args=[new_product.id]))
        else:
            messages.error(
                request,
                'Failed to add new product. Double check the form is valid.'
            )
    else:
        form = ProductForm(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'products/add_product.html', context)


@login_required
def edit_product(request, product_id):
    """ view for admin to edit products """
    # only allow super user access
    if not request.user.is_superuser:
        messages.error(
            request,
            "You must be logged in as KOR admin to do this"
        )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # validate, save and redirect user to product page
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, f"{product.name} successfully updated")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to edit product. Double check the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    """ view for admin to delete a product """
    # only allow super user access
    if not request.user.is_superuser:
        messages.error(
            request,
            "You must be logged in as KOR admin to do this"
        )
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.info(request, f"Successfully deleted \"{product.name}\"")
    return redirect(reverse('products'))
