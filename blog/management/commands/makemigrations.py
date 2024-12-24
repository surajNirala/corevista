import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command is disabled in this environment."

    def handle(self, *args, **options):
        if os.getenv("DISABLE_MAKEMIGRATIONS", "false").lower() == "true":
            self.stdout.write(self.style.ERROR("`makemigrations` command is disabled in this environment."))
            raise SystemExit(1)
        else:
            self.stdout.write(self.style.WARNING("`makemigrations` is allowed."))
