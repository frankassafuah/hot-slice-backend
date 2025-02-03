from django.urls import path
from orders.views import order_list, order

urlpatterns = [
    path("orders", order_list, name="orders"),
    path("orders/<int:pk>/", order, name="order"),
]
