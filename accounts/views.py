from dj_rest_auth.registration.views import RegisterView, LoginView
from dj_rest_auth.views import LogoutView

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
import logging

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
                    secure=True,  # Set to False for local development
                    samesite="Lax",
                    max_age=60 * 60 * 24,  # 1 day
                )

            if refresh_token:
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite="Lax",
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
                secure=True,  # Set to False for local development
                samesite="Lax",
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
