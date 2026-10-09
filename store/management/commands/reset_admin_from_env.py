

import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "One-time reset of the production Django administrator"

    def handle(self, *args, **options):
        if os.environ.get("RESET_ADMIN_NOW") != "true":
            self.stdout.write("Admin reset skipped.")
            return

        User = get_user_model()

        username = os.environ.get(
            "RESET_ADMIN_USERNAME", "eleganzo_admin"
        ).strip()
        email = os.environ.get("RESET_ADMIN_EMAIL", "").strip()
        password = os.environ.get("RESET_ADMIN_PASSWORD", "")

        if not username or not email or len(password) < 12:
            raise CommandError(
                "Set RESET_ADMIN_USERNAME, RESET_ADMIN_EMAIL "
                "and RESET_ADMIN_PASSWORD (12+ characters)."
            )

        user = User.objects.filter(username=username).first()

        if user is None:
            user = User(username=username)

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin is ready: {user.username} / {user.email}"
            )
        )