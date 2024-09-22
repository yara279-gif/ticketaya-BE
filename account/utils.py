from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class Util:
    @staticmethod
    def send_email(data):
        # Render the HTML content for the email
        html_content = data["body"]
        plain_content = strip_tags(html_content)  # Create a plain-text version by stripping HTML tags

        email = EmailMultiAlternatives(
            subject=data["subject"],
            body=plain_content,  # Plain text content
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data["to_email"]],
        )
        email.attach_alternative(html_content, "text/html")  # Attach the HTML version
        email.send(fail_silently=False)  # Set to False to raise exceptions on errors

