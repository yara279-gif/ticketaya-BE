from django.core.mail import EmailMessage
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use directly from settings
            to=[data["to_email"]],
        )
        email.send(fail_silently=False)  # Set to False to raise exceptions on errors
