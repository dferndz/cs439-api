from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        instance.new_password()
