from django.db import models
from authentication.models import User
from pizzas.models import Pizza
from django.core.validators import RegexValidator
from datetime import timedelta
from django.utils import timezone
from functools import reduce


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

    cart = models.JSONField(default=list)
    order_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_order_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    delivery_address = models.TextField(blank=False)
    customer = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
        default="Unknown",
    )
    ordered_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    priority = models.BooleanField(default=False)
    priority_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    estimated_delivery = models.DateTimeField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def reduce_stock(self):
        for item in self.cart:
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

    def set_estimated_delivery(self):
        now = timezone.now()
        base_time = timedelta(minutes=60)

        if self.priority:
            base_time = timedelta(minutes=30)
        self.estimated_delivery = now + base_time

    def set_total_order_amount(self):
        order_price = reduce(lambda x, y: x + y.get("total_price", 0), self.cart, 0)
        total_order_amount = order_price
        if self.priority:
            priority_price = order_price * 0.2
            total_order_amount = order_price + priority_price
            self.priority_price = priority_price

        self.order_price = order_price
        self.total_order_amount = total_order_amount

    def save(self, **kwargs):
        if self.pk is None:  # Only on initial order creation
            self.reduce_stock()
            self.set_estimated_delivery()
            self.set_total_order_amount()
        super().save(**kwargs)
