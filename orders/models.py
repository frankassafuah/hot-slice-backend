from django.db import models
from authentication.models import User


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

    items = models.JSONField(default=[])
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_address = models.TextField()
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
