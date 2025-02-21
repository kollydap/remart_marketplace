from django.urls import path
import products.views as product_views

urlpatterns = [
    path("products/", product_views.get_all_products, name="get_all_products"),
    path("products/<uuid:pk>/", product_views.get_product, name="get_product"),
    path("products/create/", product_views.create_product, name="create_product"),
    path(
        "products/<uuid:pk>/update/",
        product_views.update_product,
        name="update_product",
    ),
    path(
        "products/<uuid:pk>/delete/",
        product_views.delete_product,
        name="delete_product",
    ),
]
