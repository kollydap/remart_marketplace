from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from products.models import Product, ProductView, ProductCategory
from products.serializers import ProductSerializer, ProductCategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q


# GET all products with advanced filtering and pagination
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_products(request):
    """
    Retrieves a list of all products with priority-based filtering and pagination.
    """
    # Base filter: Only active products with quantity > 0
    products = Product.objects.filter(is_active=True, quantity__gt=0)

    # Role-based filtering
    # if request.user.is_authenticated and request.user.is_premium:
    if request.user.is_authenticated:

        # Premium users see all products
        pass
    else:
        # Regular users: Exclude premium products
        products = products.filter(is_premium=False)

    # Priority ordering
    featured = products.filter(is_featured=True)
    new_arrivals = products.order_by("-created_at")
    trending = products.order_by("-views")

    # Combine with priority order
    products = featured | new_arrivals | trending
    products = products.distinct()

    # Set up pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Adjust page size as needed
    paginated_products = paginator.paginate_queryset(products, request)

    # Serialize the paginated data
    serializer = ProductSerializer(paginated_products, many=True)

    # Return the paginated response
    return paginator.get_paginated_response(serializer.data)


# GET all products with pagination
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_products(request):
    """
    Retrieves a list of a user products with pagination.
    """
    # Order by creation date (or any other relevant field) to avoid UnorderedObjectListWarning
    products = (
        Product.objects.all()
        .filter(owner=request.user, quantity__gt=0)
        .order_by("-created_at")
    )  # Adjust the field as needed

    # Set up pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Adjust as needed
    paginated_products = paginator.paginate_queryset(products, request)

    # Serialize the paginated data
    serializer = ProductSerializer(paginated_products, many=True)

    # Return the paginated response
    return paginator.get_paginated_response(serializer.data)


# GET a single product by ID
@api_view(["GET"])
@permission_classes([AllowAny])
def get_product(request, pk):
    """
    Retrieves a single product by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            viewed = ProductView.objects.filter(
                product=product, user=request.user
            ).exists()
            if not viewed:
                ProductView.objects.create(product=product, user=request.user)
                product.views += 1
                product.save()
    except Product.DoesNotExist:
        return Response(
            {"message": "❌ Oops! That product has vanished."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


# CREATE a new product
@api_view(["POST"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    """
    Updates an existing product by ID, excluding is_premium, is_active, and is_featured.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"message": "❌ No product found to update."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if product.owner != request.user:
        if (
            not request.user.is_staff and not request.user.is_superuser
        ):  # Check for admin status
            return Response(
                {
                    "message": "❌ You cannot do such, This loot isn't yours to get rid of !!!"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    # Exclude restricted fields
    restricted_fields = ["is_premium", "is_active", "is_featured"]
    product_data = {
        key: value
        for key, value in request.data.items()
        if key not in restricted_fields
    }

    serializer = ProductSerializer(
        product, data=product_data, partial=True, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE a product
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    """
    Deletes a product by ID.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"message": "❌ Product already vanished!"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if product.owner != request.user:
        if (
            not request.user.is_staff and not request.user.is_superuser
        ):  # Check for admin status
            return Response(
                {
                    "message": "❌ You cannot do such, This loot isn't yours to get rid of !!!"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    product.delete()
    return Response(
        {"message": "🗑️ Product deleted. Poof! It's gone!"},
        status=status.HTTP_204_NO_CONTENT,
    )


# delete all finished products
api_view(["DELETE"])


@permission_classes([IsAdminUser])  # Only admin can delete
def delete_finished_product(request):
    """
    Deletes all products with quantity less than 1.
    """
    deleted_count, _ = Product.objects.filter(quantity__lt=1).delete()

    if deleted_count > 0:
        return Response(
            {"message": f"🧹 {deleted_count} outdated product(s) cleaned up!"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": "✨ Nothing to clean. Inventory is spotless!"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product_categories(request):
    """
    Retrieves all product categories.
    """
    categories = ProductCategory.objects.all()
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_product_categories(request):
    """
    Creates product categories.
    """
    serializer = ProductCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_products(request):
    """
    Search products by multiple keywords.
    """

    price_min = request.GET.get("min_price")

    # price_max = request.GET.get("max_price")

    # if price_min:
    #     products = products.filter(price__gte=price_min)
    # if price_max:
    #     products = products.filter(price__lte=price_max)
    query = request.GET.get("query", "")
    search_terms = query.split()  # Split by spaces to get multiple keywords

    # Build a Q object to handle multiple terms
    q_objects = Q()
    for term in search_terms:
        q_objects &= (
            Q(name__icontains=term)
            | Q(description__icontains=term)
            | Q(category__name__icontains=term)
        )

    # Filter products using the combined Q object
    products = Product.objects.filter(
        q_objects, is_active=True, quantity__gt=0
    ).distinct()

    paginator = PageNumberPagination()
    paginator.page_size = 10  # Adjust as needed
    paginated_products = paginator.paginate_queryset(products, request)

    serializer = ProductSerializer(paginated_products, many=True)
    # Serialize the paginated data

    # Return the paginated response
    return paginator.get_paginated_response(serializer.data)
