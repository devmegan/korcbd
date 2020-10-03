from django.contrib import admin
from django.urls import path
from .views import products, product_detail, add_product


urlpatterns = [
    path('', products, name='products'),
    path('product-detail/<int:pk>/', product_detail, name='product_detail'),
    path('add_product/', add_product, name='add_product'),
]
