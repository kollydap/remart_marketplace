from dj_rest_auth.registration.views import RegisterView, LoginView
from dj_rest_auth.views import LogoutView

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import logging

# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.models import TransactionPin
from accounts.serializers import TransactionPinSerializer


logger = logging.getLogger(__name__)


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)  # Call parent create method

        if response.status_code == status.HTTP_201_CREATED:
            user = self.get_user_from_response(response)  # Get user from response
            access_token = response.data.get("access")  # Get JWT access token
            refresh_token = response.data.get("refresh")  # Get JWT refresh token

            if access_token:
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    secure=False,  # Set to False for local development
                    samesite="None",
                    max_age=60 * 60 * 24,  # 1 day
                )

            if refresh_token:
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=False,
                    samesite="None",
                    max_age=60 * 60 * 24 * 7,  # 7 days
                )
            del response.data["access"]
            del response.data["refresh"]

        return response

    def get_user_from_response(self, response):
        """Extract user from response data"""
        user_data = response.data.get("user", {})
        if not user_data:
            return None

        from django.contrib.auth import get_user_model

        User = get_user_model()

        try:
            return User.objects.get(pk=user_data.get("id"))
        except User.DoesNotExist:
            return None


class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()

        # Extract token from response data
        access_token = response.data.get("access")  # Get JWT access token
        if access_token:
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,  # Set to False for local development
                samesite="None",
                max_age=60 * 60 * 24,  # 1 day
            )
            del response.data["access"]
            del response.data["refresh"]

        return response


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.delete_cookie("auth_token")  # Clear token cookie
        return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_transaction_pin(request):
    if TransactionPin.objects.filter(user=request.user).exists():
        return Response(
            {"detail": "PIN already set."}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = TransactionPinSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_transaction_pin(request):
    try:
        pin = TransactionPin.objects.get(user=request.user)
    except TransactionPin.DoesNotExist:
        return Response(
            {"detail": "No PIN found to update."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = TransactionPinSerializer(pin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
