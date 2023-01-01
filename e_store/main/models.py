from django.db import models
from django.contrib.auth.models import User


class Goods(models.Model):
    goods_choices = [
        ('Phones', 'Phones'),
        ('Laptops', 'Laptops'),
        ('PC', 'PC')
    ]
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=30, choices=goods_choices)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    p_method = [
        ('cash', 'cash'),
        ('visa', 'visa'),
        ('paypal', 'paypal')
    ]
    name = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    email = models.EmailField(max_length=30)
    phone = models.IntegerField(max_length=15)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=10)
    good = models.ForeignKey(Goods, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_method = models.CharField(choices=p_method, max_length=10)

    def __str__(self):
        return f'{self.name}'