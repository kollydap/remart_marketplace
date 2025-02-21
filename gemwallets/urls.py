from django.urls import path
import gemwallets.views as gemwallets_views

urlpatterns = [
    path("", gemwallets_views.get_my_wallet, name="get_my_wallet"),
]
