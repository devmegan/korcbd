from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """ context processor to provide cart contents to all apps """
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = quantity * product.price
        total += subtotal
        product_count += quantity
        cart_items.append({
            'product_id': product_id,
            'quantity': quantity,
            'product': product,
            'subtotal': subtotal,
        })
    context = {
        'cart_items': cart_items,
        'product_count': product_count,
        'total': total,
    }

    return context
