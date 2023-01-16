from django.db import models
from django.contrib.auth.models import User
from datetime import date


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
    image = models.ImageField(default='no_image.jpg', blank=True, null=True)

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
    phone = models.IntegerField()
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    house = models.CharField(max_length=10)
    good = models.ForeignKey(Goods, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pay_method = models.CharField(choices=p_method, max_length=10)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    date = models.DateField(default=date.today())

    def __str__(self):
        return f'{self.text}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    date = models.DateField(default=date.today())

    def __str__(self):
        return f'{self.text}'


class Rating(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.good, self.rate}"