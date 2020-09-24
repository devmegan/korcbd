import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products.models import Product


class Order(models.Model):
    order_reference = models.CharField(max_length=32, null=False, blank=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    paid = models.BooleanField(default=False, null=True)
    dispatched = models.BooleanField(default=False, null=True)

    def _generate_order_reference(self, *args, **kwargs):
        """
        Generate a random, unique order number using UUID
        """
        order_uuid = uuid.uuid4().hex.upper()
        return f"KOR-{order_uuid}"

    def update_total(self):
        """ update order total when line item is added """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
        self.save()

    def save(self, *args, **kwargs):
        """ set order number if it hasn't been set already """
        if not self.order_reference:
            self.order_reference = self._generate_order_reference()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_reference


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_price_per_unit = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """ save line item total """
        self.lineitem_price_per_unit = self.product.price
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'