from django.urls import path
from orders.views import order_list

urlpatterns = [path("orders", order_list, name="orders")]
