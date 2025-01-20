from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response, status
from orders.serializers import OrderSerializer
from orders.models import Order


@api_view(["GET", "POST"])
def order_list(request):

    if request.method == "GET":
        orders = Order.objects.filter(ordered_by=request.user).all()
        serializer = OrderSerializer(orders, many=True)
        return response.Response(serializer.data)

    if request.method == "POST":
        order = request.data
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            try:
                serializer.save(ordered_by=request.user)
                return response.Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
