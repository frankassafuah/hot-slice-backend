from rest_framework import serializers
from pizzas.models import Pizza


class PizzaSerializer(serializers.ModelSerializer):

    is_sold_out = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Pizza
        fields = "__all__"
