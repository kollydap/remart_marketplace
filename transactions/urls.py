from django.urls import path

import transactions.views as transaction_views
from accounts.views import create_transaction_pin, update_transaction_pin


urlpatterns = [
    path(
        "",
        transaction_views.get_user_transactions,
        name="get_user_transactions",
    ),
    # path("<uuid:pk>/", transaction_views.get_transaction, name="get_transaction"),
    # path("create/", transaction_views.create_transaction, name="create_transaction"),
    # path("<uuid:pk>/update/", transaction_views.update_transaction, name="update_transaction"),
    # path("<uuid:pk>/delete/", transaction_views.delete_transaction, name="delete_transaction"),
    path("pin/create/", create_transaction_pin, name="pin-create"),
    path("pin/update/", update_transaction_pin, name="pin-update"),
]
