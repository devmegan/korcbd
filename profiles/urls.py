from django.urls import path
from .views import profile, order_history


urlpatterns = [
    path('', profile, name='profile'),
    path(
        'order_history/<order_reference>/',
        order_history,
        name='order_history',
    )
]
