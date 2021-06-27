from extendProfile.models import Profile
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.fields import related
from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import pushNotification

# Create your models here.


class NotifService(models.Model):
    TYPES = {
        ("order", "ORDER"),
        ("invoice", "INVOICE"),
    }
    object_type = models.CharField(max_length=50, choices=TYPES)
    object_id = models.PositiveIntegerField()


class NotifReceiver(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    device_id = models.CharField(max_length=50, unique=True)
    profile = models.OneToOneField(Profile,
                                on_delete=models.CASCADE, blank=True, null=True)


class Notification(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    MESSAGES = {
        ("order completed", "Order Completed"),
        ("order updated", "Order Updated")
    }
    message = models.CharField(max_length=250, choices=MESSAGES)
    receivers = models.ManyToManyField(NotifReceiver, related_name="notifications")
    service = models.ForeignKey(NotifService, on_delete=models.CASCADE, blank=True, null=True)
    STATUS = {
        ("success", "SUCCESS"),
        ("failed", "FAILED"),
    }
    status = models.CharField(
        max_length=10, choices=STATUS, blank=True, null=True)
    report_url = models.CharField(max_length=250, blank=True, null=True)
    notif_id = models.CharField(max_length=50, blank=True, null=True)


@receiver(post_save, sender=Notification)
def sendNotification(sender, instance, created, **kwargs):
    if instance.receivers.all().count():
        ids = [receiver.device_id for receiver in instance.receivers.all()]
        print(ids)
        # pushNotification.apply_async((instance.message, ids, instance))
    else:
        pass
