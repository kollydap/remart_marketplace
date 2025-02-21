from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from gemwallets.models import GemWallet
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    device = serializers.CharField(max_length=250, required=True)

    # def get_cleaned_data(self):
    #     super(CustomRegisterSerializer, self).get_cleaned_data()
    #     return {
    #         "username": self.validated_data.get("username", ""),
    #         "password1": self.validated_data.get("password1", ""),
    #         "email": self.validated_data.get("email", ""),
    #         "first_name": self.validated_data.get("first_name", ""),
    #         "last_name": self.validated_data.get("last_name", ""),
    #     }

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.device = self.validated_data.get("device")
        user.save()


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    wallet_balance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "is_email_verified",
            "is_phone_verified",
            "profile_picture",
            "wallet_balance",
        ]

    def get_wallet_balance(self, obj):
        try:
            return obj.wallet.balance
        except GemWallet.DoesNotExist:
            return 0.0
