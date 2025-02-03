from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response, status
from orders.serializers import OrderSerializer
from orders.models import Order
from django.shortcuts import get_object_or_404


@api_view(["GET", "POST"])
def order_list(request):

    if request.method == "GET":
        orders = Order.objects.filter(ordered_by=request.user).all()
        serializer = OrderSerializer(orders, many=True)
        return response.Response(
            {"data": serializer.data, "status": "success"}, status=status.HTTP_200_OK
        )

    if request.method == "POST":
        order = request.data
        serializer = OrderSerializer(data=order)
        if serializer.is_valid():
            try:
                # Assign ordered_by only if the user is logged in
                if request.user.is_authenticated:
                    serializer.save(ordered_by=request.user)
                else:
                    serializer.save(ordered_by=None)  # Guest order
                return response.Response(
                    {"data": serializer.data, "status": "success"},
                    status=status.HTTP_201_CREATED,
                )
            except ValueError as e:
                return response.Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return response.Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


@api_view(["GET", "PATCH"])
def order(request, **kwargs):
    pk = kwargs.get("pk")
    order_intance = get_object_or_404(Order, id=pk)
    if request.method == "GET":
        serializer = OrderSerializer(order_intance)
        return response.Response(
            {"data": serializer.data, "status": "success"}, status=status.HTTP_200_OK
        )
