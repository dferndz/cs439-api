from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import RegradeRequest


@receiver(post_save, sender=RegradeRequest)
def auto_notify_user(sender, instance, created, **kwargs):
    if created:
        instance.notify_user()
