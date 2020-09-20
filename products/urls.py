from django.contrib import admin
from django.urls import path
from .views import products, product_detail, search_products


urlpatterns = [
    path('', products, name='products'),
    path('search/', search_products, name='search_products'),
    path('product-detail/<pk>', product_detail, name='product_detail'),
]
