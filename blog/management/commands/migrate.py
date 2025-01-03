from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "This command is disabled for this environment."

    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR("`migrate` command is disabled in this environment."))
        raise SystemExit(1)
