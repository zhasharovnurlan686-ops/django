
import os
import getpass
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Введи данные нового администратора
NEW_USERNAME = "eleganzo_admin"
NEW_EMAIL = "zhasharovnurlan686@gmail.com"

django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("База данных:", User.objects.db)

current_username = input("Текущий логин администратора (mirlan): ").strip()
new_password = getpass.getpass("Новый пароль (новый пароль): ")
confirm_password = getpass.getpass("повторите: ")

if len(new_password) < 12:
    raise SystemExit("Ошибка: пароль должен быть не короче 12 символов.")

if new_password != confirm_password:
    raise SystemExit("Ошибка: пароли не совпадают.")

if User.objects.filter(username=NEW_USERNAME).exclude(username=current_username).exists():
    raise SystemExit("Ошибка: новый логин уже занят.")

user = User.objects.get(username=current_username, is_superuser=True)
user.username = NEW_USERNAME
user.email = NEW_EMAIL
user.set_password(new_password)
user.save()

print("Логин, email и пароль изменены.")
print("Логин:", user.username)
print("Email:", user.email)