from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("api/products/", views.products_api, name="products_api"),
    path(
        "media-db/<path:path>",
        views.database_image,
        name="database_image",
    ),
]
