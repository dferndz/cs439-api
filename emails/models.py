from uuid import uuid4
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.mail import send_mail as django_send_email, settings
from smtplib import SMTPException

from django.utils.timezone import now

from emails.managers import EmailManager


class Email(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    subject = models.CharField(max_length=1024, blank=False, null=False)
    message = models.TextField(blank=True, null=True)
    recipients = ArrayField(models.EmailField(), blank=False, null=False)
    html_message = models.TextField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    sent_on = models.DateTimeField(blank=True, null=True)

    objects = EmailManager()

    def __str__(self):
        return f"Email to {self.recipients}"

    def send(self):
        try:
            django_send_email(
                subject=self.subject,
                message=self.message,
                recipient_list=self.recipients,
                html_message=self.html_message,
                from_email=settings.EMAIL_HOST_USER
            )
            self.sent = True
            self.sent_on = now()
            self.save()
            return True
        except SMTPException:
            return False
