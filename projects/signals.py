from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .choices import RegradeStatus
from .models import RegradeRequest


@receiver(pre_save, sender=RegradeRequest)
def auto_detect_status(sender, instance, **kwargs):
    try:
        original_instance = RegradeRequest.objects.get(pk=instance.pk)
        instance.old_status = original_instance.status
    except RegradeRequest.DoesNotExist:
        instance.old_status = RegradeStatus.PENDING


@receiver(post_save, sender=RegradeRequest)
def auto_notify_user(sender, instance, created, **kwargs):
    if created:
        instance.notify_user()
    else:
        if instance.status != instance.old_status:
            instance.notify_status_update()
