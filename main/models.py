from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    in_stock = models.BigIntegerField(default=0)
    added_at = models.DateField(auto_now_add=True)
    cost = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

class Finance(models.Model):
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    costs = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
