from django.db import models

from django.utils import timezone

# Create your models here.


class Warehouse(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    location = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    webpage = models.URLField(null=True)
    contact = models.CharField(max_length=200, null=True)
    phone_contact = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    contact = models.CharField(max_length=200, null=True)
    phone_contact = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )
    provider = models.ForeignKey(
        'Provider',
        on_delete=models.CASCADE,
    )
    product_type = models.ForeignKey(
        'ProductType',
        on_delete=models.CASCADE,
    )
    model = models.CharField(max_length=200, null=False)
    quantity = models.PositiveIntegerField(default=1, null=False)
    purchase_cost = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2
    )
    sale_cost = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2
    )
    friends_sale_cost = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2
    )
    is_active = models.BooleanField(default=True)
    comments = models.TextField(max_length=400)

    def get_profit(self):
        return ((self.sale_cost / self.purchase_cost) - 1) * 100

    def get_friends_profit(self):
            return ((self.friends_sale_cost / self.purchase_cost) - 1) * 100

    def __str__(self):
        return self.name
