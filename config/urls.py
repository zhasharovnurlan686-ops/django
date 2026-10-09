from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("api/products/", views.products_api, name="products_api"),
]

# Раздача загруженных фотографий товаров
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]