from django.db import models
from django.db.models import Choices

from api.user.models import User
from common.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    promotion = models.CharField(max_length=255)


class Order(TimeStampedModel):
    STATUS = [
        ('pending', 'Pending'),
        ('purchased', 'Purchased'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=255, choices=STATUS, default='pending')
