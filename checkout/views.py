from django.shortcuts import render

# Create your views here.

def checkout(request):
    return (request, 'checkout/checkout.html')