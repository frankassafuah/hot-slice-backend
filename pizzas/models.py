from django.db import models


class Pizza(models.Model):
    name = models.CharField(max_length=225, blank=False)
    ingredients = models.JSONField(default=list)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
