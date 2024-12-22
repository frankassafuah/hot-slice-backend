from django.urls import path
from pizzas.views import ListPizzasAPIView


urlpatterns = [path("menu", ListPizzasAPIView.as_view(), name="menu")]
