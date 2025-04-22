from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """

    class Meta:
        model = Transaction
        fields = [
            "id",
            "order",
            "buyer",
            "seller",
            "amount",
            "transaction_type",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]  # Fields that are read-only
