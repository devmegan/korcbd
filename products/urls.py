from django.contrib import admin
from django.urls import path
from .views import products

urlpatterns = [
    path('', products, name='products'),
]
