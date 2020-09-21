from django.shortcuts import render

# Create your views here.

def view_cart(request):
    """ view displays items in users cart """

    return render(request, 'cart/cart.html')