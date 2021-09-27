from django.contrib.auth.models import AbstractUser
from django.db import models

from commons.django.db.models import CustomBaseModel


class Client(AbstractUser):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Client {self.username}"

    class Meta:
        managed = True


class Product(CustomBaseModel):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return f"Product {self.name}"

    class Meta:
        managed = True


class Shipment(CustomBaseModel):
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Shipment #{self.pk} to {self.address}"

    class Meta:
        managed = True


class Order(CustomBaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client")
    cart = models.ManyToManyField(Product, related_name="products")
    shipment = models.ForeignKey(
        Shipment, on_delete=models.CASCADE, related_name="shipments"
    )

    def __str__(self):
        return f"Order #{self.pk} client {self.client.full_name}"

    class Meta:
        managed = True


class Payment(CustomBaseModel):
    CREDIT_CARD = 1
    DEBIT_CARD = 2
    EFFECTIVE = 3
    PAYMENT_CHOICES = [
        (CREDIT_CARD, "Credit Card"),
        (DEBIT_CARD, "Debit Card"),
        (EFFECTIVE, "Effective"),
    ]
    medium = models.CharField(max_length=2, choices=PAYMENT_CHOICES, default=3)
    order = models.ManyToManyField(Order, related_name="orders")

    def __str__(self):
        return f"Payment method {self.medium}"

    class Meta:
        managed = True
