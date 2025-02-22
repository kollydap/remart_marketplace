from django.urls import path
import orders.views as order_views

urlpatterns = [
    path("", order_views.get_all_orders, name="get_all_orders"),
    path("<uuid:pk>/", order_views.get_order, name="get_order"),
    path("create/", order_views.create_order, name="create_order"),
    # path("<uuid:pk>/update/", order_views.update_order, name="update_order"),
    # path("<uuid:pk>/delete/", order_views.delete_order, name="delete_order"),
    path("<uuid:pk>/accept/", order_views.accept_order, name="accept_order"),
    path("<uuid:pk>/decline/", order_views.decline_order, name="decline_order"),
    path(
        "<uuid:pk>/escrow/", order_views.send_gems_to_escrow, name="send_gems_to_escrow"
    ),
    path(
        "<uuid:pk>/shipped/",
        order_views.set_order_to_shipped,
        name="set_order_to_shipped",
    ),
    path(
        "<uuid:pk>/completed/",
        order_views.set_order_to_completed,
        name="set_order_to_completed",
    ),
    path(
        "<uuid:pk>/dispute/",
        order_views.set_order_to_disputed,
        name="set_order_to_disputed",
    ),
    # path("<uuid:pk>/cancel/", order_views.set_order_to_cancelled, name="set_order_to_cancelled"),
    # path("<uuid:pk>/refund/", order_views.set_order_to_refunded, name="set_order_to_refunded"),
]
