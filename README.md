# Eleganzo.mir — Django version

This project keeps the current storefront HTML/design and switches its product source from `/products.json` to Django endpoint `/api/products/`. Product management uses Django's built-in admin.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py manage.py makemigrations store
py manage.py migrate
py manage.py seed_products
py manage.py createsuperuser
py manage.py runserver
```

Storefront: http://127.0.0.1:8000/  
Admin: http://127.0.0.1:8000/admin/

## Important
- First admin account is created by `createsuperuser`; no password is hard-coded.
- `image_url` lets you keep an existing remote image URL. Uploaded images are saved under `media/` locally.
- For production, configure persistent media storage (or a compatible object storage) because local files on many cloud hosts can be ephemeral.
- `render.yaml` is a starter blueprint. Verify database plan/availability and configure a persistent media solution before relying on uploaded product images in production.
- Django replaces the old `admin.html`/GitHub-token workflow. Do not deploy the old static admin alongside this as the management interface.
- The current storefront still sends checkout through the existing WhatsApp logic; inspect checkout in staging before accepting real orders.
