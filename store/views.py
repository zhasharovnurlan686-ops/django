from django.http import JsonResponse
from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, "index.html")

def products_api(request):
    qs = Product.objects.filter(active=True).select_related("category")
    data = []
    for p in qs:
        image = p.image.url if p.image else p.image_url
        data.append({"id": p.pk, "name": p.name, "description": p.description, "price": p.price, "oldPrice": p.old_price, "stock": p.stock, "category": p.category.slug if p.category else "other", "categoryName": p.category.name if p.category else "Без категории", "image": image, "badge": p.badge, "variants": p.variants if isinstance(p.variants, list) else [], "active": p.active})
    return JsonResponse(data, safe=False)
