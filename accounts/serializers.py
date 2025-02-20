from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)

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
        user.save()

 