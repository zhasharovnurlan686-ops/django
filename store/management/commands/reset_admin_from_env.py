
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

        old_username = os.environ.get(
            "RESET_ADMIN_CURRENT_USERNAME", "mirlan"
        )
        new_username = os.environ.get("RESET_ADMIN_USERNAME", "").strip()
        new_email = os.environ.get("RESET_ADMIN_EMAIL", "").strip()
        new_password = os.environ.get("RESET_ADMIN_PASSWORD", "")

        if not new_username or not new_email or len(new_password) < 12:
            raise CommandError(
                "Set new username, email and password (12+ characters)."
            )

        try:
            user = User.objects.get(
                username=old_username,
                is_superuser=True,
            )
        except User.DoesNotExist:
            raise CommandError(
                f"Superuser '{old_username}' not found in this database."
            )

        if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            raise CommandError("The new username is already taken.")

        user.username = new_username
        user.email = new_email
        user.set_password(new_password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin updated: {user.username} / {user.email}"
            )
        )