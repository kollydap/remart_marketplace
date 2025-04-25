from django.urls import path, include
from accounts.views import CustomRegisterView
from dj_rest_auth.views import LoginView, LogoutView


urlpatterns = [
    path("signup/", CustomRegisterView.as_view(), name="custom_register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("dj_rest_auth.urls")),  # Includes other auth endpoints
   
]
# 