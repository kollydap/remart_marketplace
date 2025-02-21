from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from orders.models import Order
from orders.serializers import OrderSerializer


# GET all orders with pagination
@api_view(["GET"])
def get_all_orders(request):
    """
    Retrieves a list of all orders with pagination.
    """
    orders = Order.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Adjust as needed
    paginated_orders = paginator.paginate_queryset(orders, request)
    serializer = OrderSerializer(paginated_orders, many=True)
    return paginator.get_paginated_response(serializer.data)


# GET a single order by ID
@api_view(["GET"])
def get_order(request, pk):
    """
    Retrieves a single order by ID.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)


# CREATE a new order
@api_view(["POST"])
def create_order(request):
    """
    Creates a new order.
    """
    serializer = OrderSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE an existing order
@api_view(["PUT"])
def update_order(request, pk):
    """
    Updates an existing order by ID.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE an order
@api_view(["DELETE"])
def delete_order(request, pk):
    """
    Deletes an order by ID.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response(
        {"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )
