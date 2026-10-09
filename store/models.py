
from django.db import models


class Category(models.Model):
    name = models.CharField(
        "Название",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        "Код категории",
        max_length=120,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(
        "Название товара",
        max_length=220,
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )
    price = models.PositiveIntegerField(
        "Цена, сом",
    )
    old_price = models.PositiveIntegerField(
        "Старая цена, сом",
        null=True,
        blank=True,
    )
    stock = models.PositiveIntegerField(
        "Количество на складе",
        default=0,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    image = models.ImageField(
        "Фото товара",
        upload_to="products/",
        blank=True,
    )
    image_url = models.URLField(
        "Или ссылка на фото",
        blank=True,
    )
    badge = models.CharField(
        "Бейдж",
        max_length=80,
        blank=True,
    )
    variants = models.JSONField(
        "Варианты товара (список)",
        default=list,
        blank=True,
    )
    active = models.BooleanField(
        "Показывать на сайте",
        default=True,
    )
    created_at = models.DateTimeField(
        "Добавлен",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Обновлён",
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "товар"
        verbose_name_plural = "Товары"