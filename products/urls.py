from django.urls import path
import products.views as product_views

urlpatterns = [
    path("", product_views.get_all_products, name="get_all_products"),
    path("<uuid:pk>/", product_views.get_product, name="get_product"),
    path("<uuid:pk>/me", product_views.get_my_products, name="get_product"),
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
    path(
        "categories/",
        product_views.get_product_categories,
        name="product_categories",
    ),
    path(
        "categories/create",
        product_views.create_product_categories,
        name="create_product_categories",
    ),
    path(
        "delete/",
        product_views.delete_finished_product,
        name="delete_finished_product",
    ),
    path("search/", product_views.search_products, name="search-products"),
]
