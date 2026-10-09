import json
from pathlib import Path
from django.core.management.base import BaseCommand
from store.models import Product, Category
class Command(BaseCommand):
    help = "Import initial products from initial_products.json if database is empty"
    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write("Products already exist; import skipped.")
            return
        path = Path(__file__).resolve().parents[3] / "initial_products.json"
        if not path.exists():
            self.stdout.write("No initial_products.json found.")
            return
        for item in json.loads(path.read_text(encoding="utf-8")):
            cat_name = item.get("category") or "Без категории"
            cat, _ = Category.objects.get_or_create(name=cat_name, defaults={"slug": "other" if cat_name == "Без категории" else "category-" + str(abs(hash(cat_name)) % 1000000)})
            Product.objects.create(name=item.get("name", "Товар"), description=item.get("description", ""), price=int(item.get("price") or 0), old_price=item.get("oldPrice"), stock=int(item.get("stock") or 0), category=cat, image_url=item.get("image", "") if str(item.get("image", "")).startswith("http") else "", active=item.get("active", True), badge=item.get("badge", ""), variants=item.get("variants", []))
        self.stdout.write(self.style.SUCCESS("Initial products imported."))
