from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views
urlpatterns = [path("admin/", admin.site.urls), path("", views.home, name="home"), path("api/products/", views.products_api, name="products_api")]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
