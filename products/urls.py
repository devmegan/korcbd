from django.contrib import admin
from django.urls import path
from .views import products, product_detail


urlpatterns = [
    path('', products, name='products'),
    path('product-detail/<pk>', product_detail, name='product_detail'),
]
