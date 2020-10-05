from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time

class StripeWH_Handler:
    """handle stripe webhooks """

    def __init__(self, request):
        self.request = request
    
    def _send_confirmation_email(self, order):
        """ send confirmation email to user when order is placed """
        customer_email = order.email
        subject = render_to_string(
            'cart/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'cart/confirmation_emails/confirmation_email_body.txt',
            {'order': order,
            'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject, 
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """ handle any generic/unknown stripe wh events """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ handle payment_intent.succeeded stripe wh event """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        order_total = round(intent.charges.data[0].amount/100, 2)

        # replace empty shipping details strings with None to match db form
        for key, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[key] = None

        # Update profile information if save_info was checked and user exists
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info == "true":
                profile.profile_phone_number = shipping_details.phone
                profile.profile_country = shipping_details.address.country
                profile.profile_postcode = shipping_details.address.postal_code
                profile.profile_town_or_city = shipping_details.address.city
                profile.profile_street_address1 = shipping_details.address.line1
                profile.profile_street_address2 = shipping_details.address.line2
                profile.profile_county = shipping_details.address.state
                profile.save()

        # create a webhook if order hasn't been saved
        order_exists = False
        attempt = 1
        # keep trying to find order x5 over 5s
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    order_total=order_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            # now order exists, send a confirmation email to user
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: verified order already exists in database',
                status=200)
        else:
            order = None
            try:
                # if order doesn't exist after 5x searches over 5s, go ahead and create it
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for product_id, quantity in json.loads(cart).items():
                    product = Product.objects.get(id=product_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        lineitem_price_per_unit=product.price,
                        lineitem_total=quantity * product.price
                    )
                    order_line_item.save()
            except Exception as e:
                # if any error, delete order that's just been created
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        # now order created by webhooks, send a confirmation email to user
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ handle payment_intent.payment_failed stripe wh event """
        return HttpResponse(
            content=f'Payment failed webhook received: {event["type"]}',
            status=200)
