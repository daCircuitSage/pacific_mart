from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser if it does not exist'

    def handle(self, *args, **options):
        email = config('SUPERUSER_EMAIL', default='admin@example.com')
        password = config('SUPERUSER_PASSWORD', default='admin123')
        first_name = config('SUPERUSER_FIRST_NAME', default='Admin')
        last_name = config('SUPERUSER_LAST_NAME', default='User')

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {email} already exists'))
