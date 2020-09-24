from django.contrib import admin
from django.urls import path
from .views import view_cart, add_to_cart, update_cart, remove_from_cart

urlpatterns = [
    path('', view_cart, name='cart'),
    path('add_to_cart/<product_id>', add_to_cart, name='add_to_cart'),
    path('update/<product_id>', update_cart, name='update_cart'),
    path('remove/<product_id>', remove_from_cart, name='remove_from_cart'),
]