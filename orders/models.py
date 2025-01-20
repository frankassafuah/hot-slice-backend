from django.db import models
from authentication.models import User
from pizzas.models import Pizza


class Order(models.Model):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PREPARING, "Preparing"),
        (READY, "Ready"),
        (DELIVERED, "delivered"),
        (CANCELLED, "cancelled"),
    ]

    items = models.JSONField(default=list)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_address = models.TextField(blank=False)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def reduce_stock(self):
        for item in self.items:
            item_id = item.get("id")
            item_quantity = item.get("quantity", 0)

            try:
                pizza = Pizza.objects.get(id=item_id)

                if pizza.stock_quantity >= item_quantity:
                    pizza.stock_quantity -= item_quantity
                    pizza.save()
                else:
                    raise ValueError(f"Not enough stock for pizza: {pizza.name}")

            except Pizza.DoesNotExist:
                raise ValueError(f"Pizza with id {item_id} does not exist")

    def save(self, **kwargs):
        if self.pk is None:
            self.reduce_stock()
        super().save(**kwargs)
