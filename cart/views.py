from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from products.models import Product
from .models import OrderLineItem, Order
from profiles.models import UserProfile
from .forms import OrderForm
from profiles.forms import UserProfileForm

from cart.contexts import cart_contents

import stripe
import json


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
        messages.success(request, f"{product} (x{quantity}) removed from cart")

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, product_id):
    """ remove product from shopping cart """
    try:
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get('cart', {})
        cart.pop(product_id)
        messages.success(request, f"{product} removed from cart")

        request.session['cart'] = cart
        return redirect(reverse('cart'))

    except Exception as e:
        print(e)
        messages.error(request, f"Error removing item from cart {e}")
        return redirect(reverse('cart'))


@require_POST
def cache_checkout_data(request):
    """ cache client secret from payment intent as pid """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, there\'s been a problem processing your payment. \
        Please try again in a few minutes.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ a view to process customer order details and stripe payment """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    if not stripe_public_key:
        print("Error fetching stripe public key \
        - is it definitely exported to settings?")

    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if not stripe_secret_key:
        print("Error fetching stripe secret key \
        - is it definitely exported to settings?")

    cart = request.session.get('cart', {})
    current_cart = cart_contents(request)
    total = current_cart['total']
    if request.method == 'POST':
        form = request.POST
        form_data = {
            'full_name': form['full_name'],
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
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
                    messages.error(
                        request,
                        "One of the products your trying to order has been discontinuted \
                        Please call for assistance!"
                    )
                    order.delete()
                    return redirect(reverse('cart'))
            return redirect(
                reverse(
                    'checkout_success',
                    args=[order.order_reference]
                )
            )
        else:
            messages.error(request, "There was an error processing your order. \
            Please double-check your information")
    else:
        if not cart:
            """ prevent users manually accessing checkout url """
            messages.error(
                request,
                "There's nothing in your cart at the moment"
            )
            return redirect(reverse('products'))

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name':
                        profile.user.first_name + " " + profile.user.last_name,
                    'email':
                        profile.user.email,
                    'phone_number':
                        profile.profile_phone_number,
                    'country':
                        profile.profile_country,
                    'postcode':
                        profile.profile_postcode,
                    'town_or_city':
                        profile.profile_town_or_city,
                    'street_address1':
                        profile.profile_street_address1,
                    'street_address2':
                        profile.profile_street_address2,
                    'county':
                        profile.profile_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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
    save_info = request.session.get('save_info')
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Link the new order to users profile
        order.user_profile = profile
        order.save()

    if save_info == "true":
        profile_data = {
            'profile_phone_number': order.phone_number,
            'profile_country': order.country,
            'profile_postcode': order.postcode,
            'profile_town_or_city': order.town_or_city,
            'profile_street_address1': order.street_address1,
            'profile_street_address2': order.street_address2,
            'profile_county': order.county,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    if 'cart' in request.session:
        del request.session['cart']

    context = {
        'order': order,
    }
    return render(request, 'cart/checkout_success.html', context)
