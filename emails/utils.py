from django.template.loader import render_to_string

from emails.models import Email


def send_email(subject, template, context, recipients):
    html_message = render_to_string(template, context=context)
    Email.objects.create(
        subject=subject,
        html_message=html_message,
        recipients=recipients
    )
