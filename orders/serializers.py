from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    buyer_username = serializers.ReadOnlyField(source="buyer.username")

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "buyer_username",
            "product",
            "product_name",
            "quantity",
            "total_gems",
            "state",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
