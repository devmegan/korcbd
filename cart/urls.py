from django.contrib import admin
from django.urls import path
from .views import view_cart, add_to_cart

urlpatterns = [
    path('', view_cart, name='cart'),
    path('add_to_cart/<product_id>', add_to_cart, name='add_to_cart'),
]
