from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from decouple import config

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        try:
            email = EmailMessage(
                subject='Test Email from Django',
                body='This is a test email to verify email configuration.',
                to=[config('EMAIL_HOST_USER', default='test@example.com')],
                from_email=None
            )
            email.send()
            
            self.stdout.write(self.style.SUCCESS('✅ Email sent successfully!'))
            self.stdout.write(f'Email settings:')
            self.stdout.write(f'  HOST: {config("EMAIL_HOST")}')
            self.stdout.write(f'  PORT: {config("EMAIL_PORT")}')
            self.stdout.write(f'  USER: {config("EMAIL_HOST_USER")}')
            self.stdout.write(f'  TLS: {config("EMAIL_USE_TLS")}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Email failed: {str(e)}'))
            self.stdout.write(f'Email settings:')
            self.stdout.write(f'  HOST: {config("EMAIL_HOST")}')
            self.stdout.write(f'  PORT: {config("EMAIL_PORT")}')
            self.stdout.write(f'  USER: {config("EMAIL_HOST_USER")}')
            self.stdout.write(f'  PASSWORD: {"SET" if config("EMAIL_HOST_PASSWORD") else "NOT SET"}')
            self.stdout.write(f'  TLS: {config("EMAIL_USE_TLS")}')
