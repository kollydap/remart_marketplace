from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomRegisterView, CustomLoginView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
