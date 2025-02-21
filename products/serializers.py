from rest_framework import serializers
from products.models import ProductCategory, Product


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "description"]


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price_in_gems",
            "state",
            "image",
            "category",
            "category_id",
            "owner",
            "location",
            "quantity",
            "is_premium",
            "is_active",
            "is_featured",
            "views",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        category_id = validated_data.pop("category_id")
        validated_data["category"] = ProductCategory.objects.get(id=category_id)
        validated_data["owner"] = self.context["request"].user
        return Product.objects.create(**validated_data)
