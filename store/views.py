from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render

from .models import Product, MediaBlob


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
            image = product.image_url or ""

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


def database_image(request, path):
    try:
        image = MediaBlob.objects.get(path=path)
    except MediaBlob.DoesNotExist:
        raise Http404("Изображение не найдено")

    response = HttpResponse(
        bytes(image.data),
        content_type=image.content_type,
    )
    response["X-Content-Type-Options"] = "nosniff"
    response["Cache-Control"] = "public, max-age=86400"

    return response