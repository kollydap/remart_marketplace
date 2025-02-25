from rest_framework import serializers
from orders.models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    buyer_username = serializers.ReadOnlyField(source="buyer.username")
    owner = serializers.ReadOnlyField(source="product.owner.id")  # Owner's ID
    owner_username = serializers.ReadOnlyField(source="product.owner.username")
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "buyer_username",
            "owner",
            "owner_username",
            "product",
            "product_name",
            "quantity",
            "total_gems",
            "state",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "buyer",
            "total_gems",
            "owner",
        ]

    def create(self, validated_data):
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")
        user = self.context["request"].user

        # Check if the user is the owner of the product
        if product.owner == user:
            raise serializers.ValidationError(
                {"message": "Nice try, but you can't buy your own loot!"}
            )

        # Check if the requested quantity exceeds available stock
        if quantity > product.quantity:
            raise serializers.ValidationError(
                {
                    "message": "Whoa! That's more than what's in stock. Try a smaller number!"
                }
            )
        

        # Calculate total gem price
        price_in_gem = product.price_in_gems
        total_gem_price = price_in_gem * quantity

         # Check if the user has enough gems in their wallet
        if user.wallet.balance < total_gem_price:
            raise serializers.ValidationError(
                {
                    "message": "Uh-oh! Not enough gems. Complete more quests to earn gems!"
                }
            )

        # Set total gems and buyer
        validated_data["total_gems"] = total_gem_price
        validated_data["buyer"] = user
        validated_data["product"] = product

        # Deduct the total gems from the user's wallet
        user.wallet.balance -= total_gem_price
        user.save()

        return Order.objects.create(**validated_data)
