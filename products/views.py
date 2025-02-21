from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from products.models import Product
from products.serializers import ProductSerializer


# GET all products with pagination
@api_view(["GET"])
def get_all_products(request):
    """
    Retrieves a list of all products with pagination.
    """
    products = Product.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Adjust as needed
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)


# GET a single product by ID
@api_view(["GET"])
def get_product(request, pk):
    """
    Retrieves a single product by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(product)
    return Response(serializer.data)


# CREATE a new product
@api_view(["POST"])
def create_product(request):
    """
    Creates a new product.
    """
    serializer = ProductSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE an existing product
@api_view(["PUT"])
def update_product(request, pk):
    """
    Updates an existing product by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ProductSerializer(
        product, data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE a product
@api_view(["DELETE"])
def delete_product(request, pk):
    """
    Deletes a product by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
        )

    product.delete()
    return Response(
        {"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )
