from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates a superuser if one does not exist."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            self.stdout.write("Creating default superuser 'admin'...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists."))
