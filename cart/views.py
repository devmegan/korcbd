from django.shortcuts import render, redirect, reverse

# Create your views here.


def view_cart(request):
    """ view displays items in users cart """

    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ add quantity of product to shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, product_id):
    """ remove product from shopping cart """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id)

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, product_id):
    """ remove product from shopping cart """
    cart = request.session.get('cart', {})
    cart.pop(product_id)

    request.session['cart'] = cart
    return redirect(reverse('cart'))
