from django.urls import path
import orders.views as order_views

urlpatterns = [
    path("orders/", order_views.get_all_orders, name="get_all_orders"),
    path("orders/<uuid:pk>/", order_views.get_order, name="get_order"),
    path("orders/create/", order_views.create_order, name="create_order"),
    path("orders/<uuid:pk>/update/", order_views.update_order, name="update_order"),
    path("orders/<uuid:pk>/delete/", order_views.delete_order, name="delete_order"),
]
