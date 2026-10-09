
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "stock",
        "category",
        "active",
        "updated_at",
    )

    list_filter = ("active", "category")
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "active")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "description",
                    "category",
                    "active",
                    "badge",
                )
            },
        ),
        (
            "Цена и наличие",
            {"fields": ("price", "old_price", "stock")},
        ),
        (
            "Фото",
            {"fields": ("image", "image_url")},
        ),
        (
            "Варианты",
            {"fields": ("variants",)},
        ),
        (
            "Даты",
            {"fields": ("created_at", "updated_at")},
        ),
    )


admin.site.site_header = "Eleganzo.mir — управление магазином"
admin.site.site_title = "Eleganzo Admin"
admin.site.index_title = "Товары и категории"
