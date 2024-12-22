from django.shortcuts import render
from rest_framework import generics, response, status
from pizzas.serializers import PizzaSerializer
from pizzas.models import Pizza


class ListPizzasAPIView(generics.ListAPIView):
    serializer_class = PizzaSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Pizza.objects.all()
        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset
