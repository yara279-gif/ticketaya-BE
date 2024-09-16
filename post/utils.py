from django.core.mail import EmailMessage
from django.conf import settings

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data['to_email']]
        )
        try:
            email.send(fail_silently=False)
        except Exception as e:
            print(f"Error sending email: {e}")
