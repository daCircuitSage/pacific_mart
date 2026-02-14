from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from decouple import config
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        self.stdout.write("Testing email configuration...")
        
        # Print email settings (without password)
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        self.stdout.write(f"EMAIL_HOST_PASSWORD exists: {bool(config('EMAIL_HOST_PASSWORD', default=''))}")
        
        try:
            # Test email sending
            subject = 'Test Email from PacificMart'
            message = 'This is a test email to verify the email configuration is working.'
            from_email = None
            recipient_list = ['shihabthebrowncrow@gmail.com']  # Change to your test email
            
            email = EmailMessage(
                subject,
                message,
                to=recipient_list,
                from_email=from_email
            )
            
            self.stdout.write("Attempting to send test email...")
            result = email.send(fail_silently=False)
            
            if result:
                self.stdout.write(self.style.SUCCESS(f"Email sent successfully! Return value: {result}"))
            else:
                self.stdout.write(self.style.ERROR("Email sending failed - no return value"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Email sending failed: {type(e).__name__}: {e}"))
            logger.error(f"Email test failed: {e}", exc_info=True)
