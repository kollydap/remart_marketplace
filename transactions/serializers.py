from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """

    class Meta:
        model = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]  # Fields that are read-only
