from rest_framework import serializers
from .models import GemWallet


class GemWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = GemWallet
        fields = [
            "id",
            "balance",
            "state",
            "status",
        ]
        read_only_fields = ["id", "balance", "user", "created_at", "updated_at"]
