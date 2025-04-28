from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from orders.models import Order, OrderState, OrderDisputes
from orders.serializers import OrderSerializer
from products.models import Product
from django.db.models import Q
from accounts.models import TransactionPin


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


# GET all orders for a specific user
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    """
    Retrieves a list of all orders for the authenticated user
    either as a buyer or as a product owner.
    """
    user = request.user
    orders = Order.objects.filter(Q(buyer=user) | Q(product__owner=user)).distinct()

    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_orders = paginator.paginate_queryset(orders, request)
    serializer = OrderSerializer(paginated_orders, many=True)

    return paginator.get_paginated_response(serializer.data)


# GET all orders for a specific product
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_product_orders(request, pk):
    """
    Retrieves a list of all orders for a specific product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )

    orders = Order.objects.filter(product=product)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_orders = paginator.paginate_queryset(orders, request)
    serializer = OrderSerializer(paginated_orders, many=True)
    return paginator.get_paginated_response(serializer.data)


# GET a single order by ID
@api_view(["GET"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
# @api_view(["PUT"])
# @permission_classes([IsAuthenticated])
# def update_order(request, pk):
#     """
#     Updates an existing order by ID.
#     """
#     try:
#         order = Order.objects.get(pk=pk)
#     except Order.DoesNotExist:
#         return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

#     serializer = OrderSerializer(order, data=request.data, context={"request": request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE an order
@api_view(["DELETE"])
def delete_order(request, pk):
    """
    Deletes an order by ID.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND
        )
    # Check if the current user is the owner of the order
    if order.buyer != request.user or order.product.owner != request.user:
        return Response(
            {"message": "You do not have permission to delete this order."},
            status=status.HTTP_403_FORBIDDEN,
        )

    order.delete()
    return Response(
        {"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )


# **----------------------------------------------------------------------------------**


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def accept_order(request, pk):
    """
    Accepts an Order by Id
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Quest failed! The order you seek is lost in the abyss."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if order is still in pending state
    if order.state != OrderState.PENDING:
        return Response(
            {
                "message": "Oops! This order is no longer in the waiting realm. You can't alter its destiny now."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the current user is the owner of the product
    if order.product.owner != request.user:
        return Response(
            {"message": "Halt, You lack the power to accept this order."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the product is in stock
    if order.product.quantity < order.quantity:
        return Response(
            {
                "message": "Out of stock! You've lost a customer’s trust. Better restock before another adventurer leaves empty-handed."
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    # Accept the order
    order.state = OrderState.ACCEPTED
    order.save()
    # Send notification to the buyer that the order has been accepted
    # (You can add your notification logic here)

    return Response(
        {
            "message": "Order accepted! Your heroic deed has been recorded. The adventurer will be notified of their prize!"
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def decline_order(request, pk):
    """
    Declines an Order by Id
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Quest failed! The order you seek is lost in the abyss."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if order is still in pending state
    if order.state != OrderState.PENDING:
        return Response(
            {
                "message": "The sands of time have shifted. This order's destiny is sealed."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the current user is the owner of the product
    if order.product.owner != request.user:
        return Response(
            {"message": "Halt, You lack the powers to decline an order."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Decline the order
    order.state = OrderState.DECLINED
    order.save()

    # Optionally, you can notify the buyer that the order has been declined
    # (You can add your notification logic here)

    return Response(
        {
            "message": "Order declined! The adventurer's hopes have been dashed, but your realm remains secure."
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_gems_to_escrow(request, pk):
    """
    Sends gems to escrow
    """
    # Check if the user has set a transaction pin
    pin = request.data.get("pin")
    if not pin:
        return Response(
            {"detail": "Pin is required."}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        transaction_pin = TransactionPin.objects.get(user=request.user)
    except TransactionPin.DoesNotExist:
        return Response(
            {"detail": "Transaction pin not set. Please set up your pin first."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if transaction_pin.pin != pin:
        return Response(
            {"detail": "Incorrect pin. Access denied."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Quest failed! The order you seek is lost in the abyss."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if order is in accepted state
    if order.state != OrderState.ACCEPTED:
        return Response(
            {
                "message": "The stars haven't aligned! Gems can only be sent for accepted orders."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the current user is the buyer of the product
    if order.buyer != request.user:
        return Response(
            {
                "message": "Halt, adventurer! These gems are not yours to offer. Only the rightful buyer can proceed."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the buyer has enough gems
    if order.buyer.wallet.balance < order.total_gems:
        return Response(
            {
                "message": "Insufficient gems! You must gather more wealth before embarking on this quest."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Deduct gems from buyer's wallet
    order.buyer.wallet.balance -= order.total_gems
    order.buyer.wallet.save()

    # !todo credit the admin wallet

    # Move the order to escrowed state
    order.state = OrderState.ESCROWED
    order.save()

    # Optionally, you can notify the seller that the gems have been escrowed
    # (You can add your notification logic here)

    return Response(
        {
            "message": "Success! Your gems are safely stored in the ancient vault, awaiting the seller's heroic delivery."
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def set_order_to_shipped(request, pk):
    """
    Sets the order state to shipped by the seller
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Quest failed! The order you seek is lost in the abyss."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if the order is in the escrowed state
    if order.state != OrderState.ESCROWED:
        return Response(
            {
                "message": "Patience, hero! Only orders with gems secured in the vault can be shipped."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the current user is the owner of the product
    if order.product.owner != request.user:
        return Response(
            {
                "message": "Hold your horses! You are not the rightful merchant for this quest."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if the product is still in stock
    if order.product.quantity < order.quantity:
        return Response(
            {
                "message": "Uh-oh! Your stockpile is empty. Restock before you let the adventurer down."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    # Deduct the product quantity
    order.product.quantity -= order.quantity
    order.product.save()

    # Set the order state to shipped
    order.state = OrderState.SHIPPED
    order.save()

    # Optionally, you can notify the buyer that the order has been shipped
    # (You can add your notification logic here)

    return Response(
        {
            "message": "Huzzah! The package is on its journey. May the winds guide it swiftly to the buyer’s doorstep."
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def set_order_to_completed(request, pk):
    """
    Sets the order state to completed
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Quest failed! The order you seek is lost in the abyss."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Only the buyer can mark the order as completed
    if order.buyer != request.user:
        return Response(
            {
                "message": "Only the adventurer who made the purchase can complete this quest."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    if order.state == OrderState.COMPLETED:
        return Response(
            {"message": "Hold on! This order has been completed."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Check if order is in shipped state
    if order.state != OrderState.SHIPPED:
        return Response(
            {
                "message": "Hold on! The package hasn't arrived yet. Wait for its safe delivery."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    order.buyer.wallet.balance += order.total_gems
    order.buyer.wallet.save()

    order.state = OrderState.COMPLETED
    order.save()

    return Response(
        {"message": "Congratulations!. Your gems are well spent!"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_order_to_disputed(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"message": "Order lost in the abyss."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.user not in [order.buyer, order.product.owner]:
        return Response(
            {"message": "This is not your battle."},
            status=status.HTTP_403_FORBIDDEN,
        )

    order.state = OrderState.DISPUTED
    order.save()
    OrderDisputes.objects.create(order=order, message=request.data.get("message"))

    return Response(
        {"message": "Dispute raised. Awaiting council's verdict."},
        status=status.HTTP_200_OK,
    )
