from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.view_cart, name='cart'),
    path('add_to_cart/<product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<product_id>/', views.update_cart, name='update_cart'),
    path(
        'remove/<product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
    path('checkout/', views.checkout, name='checkout'),
    path(
        'checkout_success/<order_reference>/',
        views.checkout_success,
        name='checkout_success'
    ),
    path(
        'cache_checkout_data/',
        views.cache_checkout_data,
        name='cache_checkout_data'
    ),
    path('wh/', webhook, name='webhook'),
]
