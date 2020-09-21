from django.contrib import admin
from django.urls import path
from .views import view_cart

urlpatterns = [
    path('', view_cart, name='cart'),
]
