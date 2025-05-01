from rest_framework import serializers
from products.models import ProductCategory, Product, ProductImage


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "description"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "order"]


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True)
    owner = serializers.StringRelatedField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.CharField(max_length=500), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price_in_gems",
            "state",
            "image",  # Keeping this for backward compatibility
            "images",  # New field for multiple images
            "uploaded_images",  # For creating multiple images
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
        uploaded_images = validated_data.pop("uploaded_images", [])

        # Keep the main image field for backward compatibility
        main_image = validated_data.get("image")

        try:
            validated_data["category"] = ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "message": "The provided category does not exist. Please check and try again."
                }
            )

        validated_data["owner"] = self.context["request"].user
        product = Product.objects.create(**validated_data)

        # Create product images
        if uploaded_images:
            # If there are uploaded images, create image objects
            for i, image_url in enumerate(uploaded_images):
                is_primary = False
                if i == 0 and not main_image:  # First image is primary if no main image
                    is_primary = True
                ProductImage.objects.create(
                    product=product, image=image_url, is_primary=is_primary, order=i
                )

        # If main image exists and no images uploaded with is_primary
        if (
            main_image
            and not ProductImage.objects.filter(
                product=product, is_primary=True
            ).exists()
        ):
            ProductImage.objects.create(
                product=product, image=main_image, is_primary=True, order=0
            )

        return product

    def update(self, instance, validated_data):
        # Handle uploaded images if any
        uploaded_images = validated_data.pop("uploaded_images", None)

        # Update the existing instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Process uploaded images if provided
        if uploaded_images is not None:
            # Optionally clear existing images if replacing all
            # ProductImage.objects.filter(product=instance).delete()

            for i, image_url in enumerate(uploaded_images):
                ProductImage.objects.create(
                    product=instance,
                    image=image_url,
                    order=ProductImage.objects.filter(product=instance).count() + i,
                )

        return instance
