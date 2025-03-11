from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomRegisterView, CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/products/", include("products.urls")),
    path("api/v1/orders/", include("orders.urls")),
    # path("api/v1/transactions/", include("transactions.urls")),
    path("api/v1/wallets/", include("gemwallets.urls")),
    # Authentication endpoints
    path("api/v1/auth/signin/", CustomLoginView.as_view(), name="custom_login"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    # Login, logout, password reset, etc.
    path(
        "api/v1/auth/signup/", CustomRegisterView.as_view(), name="custom_register"
    ),  # Custom signup view
    path(
        "api/v1/auth/registration/", include("dj_rest_auth.registration.urls")
    ),  # Default registration
]
