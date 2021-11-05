from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Email


@receiver(post_save, sender=Email)
def auto_send_mail(sender, instance, created, **kwargs):
    if created:
        instance.send()
