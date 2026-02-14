from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from decouple import config
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def test_email_view(request):
    """Test email configuration via web interface"""
    if request.method == 'POST':
        try:
            # Get email from form or use default
            test_email = request.POST.get('email', 'shihabthebrowncrow@gmail.com')
            
            # Collect email settings for debugging
            email_settings = {
                'EMAIL_BACKEND': settings.EMAIL_BACKEND,
                'EMAIL_HOST': settings.EMAIL_HOST,
                'EMAIL_PORT': settings.EMAIL_PORT,
                'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
                'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
                'EMAIL_USE_SSL': settings.EMAIL_USE_SSL,
                'EMAIL_HOST_PASSWORD_EXISTS': bool(config('EMAIL_HOST_PASSWORD', default='')),
                'DEBUG': settings.DEBUG,
            }
            
            logger.info(f"Email test started with settings: {email_settings}")
            
            # Test email sending
            subject = 'Test Email from PacificMart'
            message = f'''
This is a test email to verify the email configuration is working.

Email Settings:
- Backend: {email_settings['EMAIL_BACKEND']}
- Host: {email_settings['EMAIL_HOST']}
- Port: {email_settings['EMAIL_PORT']}
- User: {email_settings['EMAIL_HOST_USER']}
- TLS: {email_settings['EMAIL_USE_TLS']}
- SSL: {email_settings['EMAIL_USE_SSL']}
- Password Set: {email_settings['EMAIL_HOST_PASSWORD_EXISTS']}
- Debug Mode: {email_settings['DEBUG']}

If you receive this email, the configuration is working!
            '''
            
            email = EmailMessage(
                subject,
                message,
                to=[test_email],
                from_email=None
            )
            
            result = email.send(fail_silently=False)
            
            response_data = {
                'success': True,
                'message': f'Email sent successfully to {test_email}! Return value: {result}',
                'settings': email_settings
            }
            
            logger.info(f"Email test successful: {response_data}")
            
            return JsonResponse(response_data)
            
        except Exception as e:
            error_data = {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
                'settings': {
                    'EMAIL_BACKEND': settings.EMAIL_BACKEND,
                    'EMAIL_HOST': settings.EMAIL_HOST,
                    'EMAIL_PORT': settings.EMAIL_PORT,
                    'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
                    'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
                    'EMAIL_USE_SSL': settings.EMAIL_USE_SSL,
                    'EMAIL_HOST_PASSWORD_EXISTS': bool(config('EMAIL_HOST_PASSWORD', default='')),
                }
            }
            
            logger.error(f"Email test failed: {error_data}", exc_info=True)
            
            return JsonResponse(error_data)
    
    return render(request, 'accounts/test_email.html')
