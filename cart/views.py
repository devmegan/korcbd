from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from products.models import Product
from .models import OrderLineItem, Order
from .forms import OrderForm

from cart.contexts import cart_contents

import stripe


def view_cart(request):
    """ view displays items in users cart """

    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ add quantity of product to shopping cart """
    product = Product.objects.get(pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    messages.success(request, f"{product} (x{quantity}) added to cart")
    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, product_id):
    """ remove product from shopping cart """
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id)
        messages.error(request, f"{product} (x{quantity}) removed from cart")

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, product_id):
    """ remove product from shopping cart """
    try:
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        cart.pop(product_id)
        messages.error(request, f"{product} removed from cart")

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        print(e)
        messages.error(request, f"Error removing item from cart \ {e}")
        return HttpResponse(status=500)


def checkout(request):
    """ a view to process customer order details and stripe payment """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    if not stripe_public_key:
        print("Error fetching stripe public key - is it definitely exported to settings?")

    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if not stripe_secret_key:
        print("Error fetching stripe secret key - is it definitely exported to settings?")

    cart = request.session.get('cart', {})
    current_cart = cart_contents(request)
    total = current_cart['total']

    if request.method == 'POST':
        form = request.POST
        form_data = {
            'first_name': form['first_name'],
            'last_name': form['last_name'],
            'email': form['email'],
            'phone_number': form['phone_number'],
            'country': form['country'],
            'postcode': form['postcode'],
            'town_or_city': form['town_or_city'],
            'street_address1': form['street_address1'],
            'street_address2': form['street_address2'],
            'county': form['county'],
            'paid': True,
            'order_total': total,
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for product_id, quantity in cart.items():
                try:
                    product = get_object_or_404(Product, pk=product_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        lineitem_price_per_unit=product.price,
                        lineitem_total=quantity * product.price
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, "One of the products your trying to order has been discontinuted \ Please call for assistance!")
                    order.delete()
                    return redirect(reverse('cart'))
            return redirect(reverse('checkout_success', args=[order.order_reference]))
        else:
            messages.error(request, "There was an error processing your order. Please double-check your information")
    else:
        if not cart:
            """ prevent users manually accessing checkout url """
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('products'))

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,

            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'stripe_client_secret': intent.client_secret
        }
        return render(request, 'cart/checkout.html', context)


def checkout_success(request, order_reference):
    """ view to display order confirmation to user """
    order = get_object_or_404(Order, order_reference=order_reference)
    messages.success(request, f'Order successfully processed. Your order reference is {order_reference} \ An order confirmation will be sent to {order.email}')

    if 'cart' in request.session:
        del request.session['cart']

    context = {
        'order': order,
    }
    return render(request, 'cart/checkout_success.html', context)
