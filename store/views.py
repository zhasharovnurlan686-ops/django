
from django.http import JsonResponse
from django.shortcuts import render

from .models import Product


def home(request):
    return render(request, "index.html")


def products_api(request):
    products = (
        Product.objects
        .filter(active=True)
        .select_related("category")
    )

    data = []

    for product in products:
        if product.image:
            image = product.image.url
        else:
            image = product.image_url

        data.append({
            "id": product.pk,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "oldPrice": product.old_price,
            "stock": product.stock,
            "category": (
                product.category.slug
                if product.category
                else "other"
            ),
            "categoryName": (
                product.category.name
                if product.category
                else "Без категории"
            ),
            "image": image,
            "badge": product.badge,
            "variants": (
                product.variants
                if isinstance(product.variants, list)
                else []
            ),
            "active": product.active,
        })

    return JsonResponse(data, safe=False)