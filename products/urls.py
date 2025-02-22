from django.urls import path
import products.views as product_views

urlpatterns = [
    path("", product_views.get_all_products, name="get_all_products"),
    path("<uuid:pk>/", product_views.get_product, name="get_product"),
    path("create/", product_views.create_product, name="create_product"),
    path(
        "<uuid:pk>/update/",
        product_views.update_product,
        name="update_product",
    ),
    path(
        "<uuid:pk>/delete/",
        product_views.delete_product,
        name="delete_product",
    ),
]
