from rest_framework import serializers
from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    order_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "order",
            "sender",
            "receiver",
            "amount",
            "state",
            "status",
            "signature",
            "created_at",
            "updated_at",
            "sender_name",
            "receiver_name",
            "product_name",
            "order_quantity",
        ]

    def get_sender_name(self, obj):
        return obj.sender.user.get_full_name() or obj.sender.user.username

    def get_receiver_name(self, obj):
        return obj.receiver.user.get_full_name() or obj.receiver.user.username

    def get_product_name(self, obj):
        try:
            return obj.order.product.name
        except AttributeError:
            return "Unknown Product"

    def get_order_quantity(self, obj):
        try:
            return obj.order.quantity
        except AttributeError:
            return "Unknown Quantity"
