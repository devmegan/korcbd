from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.
class OrderLineItemAdminInline(admin.TabularInline):
    """ allow editing line items on order model """
    model = OrderLineItem
    readonly_fields = ('lineitem_total', 'lineitem_price_per_unit')

class OrderAdmin(admin.ModelAdmin):
    inlines = OrderLineItemAdminInline,
    readonly_fields = (
        'date',
        'order_total',
    )
    fields = (
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
        'paid',
        'dispatched',
    )
    list_display = (
        'order_reference',
        'last_name',
        'date',
        'paid',
        'dispatched',
    )

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
