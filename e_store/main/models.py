from django.db import models


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

