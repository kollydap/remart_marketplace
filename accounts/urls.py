from django.urls import path, include
from accounts.views import CustomRegisterView
from dj_rest_auth.views import LoginView, LogoutView
from accounts.views import create_transaction_pin, update_transaction_pin


urlpatterns = [
    path("signup/", CustomRegisterView.as_view(), name="custom_register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("dj_rest_auth.urls")),  # Includes other auth endpoints
    path("pin/create/", create_transaction_pin, name="pin-create"),
    path("pin/update/", update_transaction_pin, name="pin-update"),
]
