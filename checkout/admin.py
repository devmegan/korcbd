from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.
class OrderLineItemAdminInline(admin.TabularInline):
    """ allow editing line items on order model """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

class OrderAdmin(admin.ModelAdmin):
    inlines = OrderLineItemAdminInline,
    readonly_fields = (
        'order_reference',
        'date',
        'order_total',
    )
    fields = (
        'order_reference',
        'date',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'street_address1',
        'street_address2',
        'town_or_city',
        'county',
        'country',
        'postcode',
        'order_total',
    )
    list_display = (
        'order_reference',
        'date',
        'first_name',
        'last_name',
        'order_total',
    )

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
