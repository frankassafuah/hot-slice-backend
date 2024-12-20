from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['ordered_by']
