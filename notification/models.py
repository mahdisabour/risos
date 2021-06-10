from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.fields import related
from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import pushNotification

# Create your models here.


class Service(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Receiver(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    device_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Notification(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at")
    message = models.CharField(max_length=250)
    receivers = models.ManyToManyField(Receiver, related_name="notifications")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    STATUS = {
        ("success", "SUCCESS"),
        ("failed", "FAILED"),
    }
    status = models.CharField(max_length=10, choices=STATUS, blank=True, null=True)
    report_url = models.CharField(max_length=250, blank=True, null=True)
    notif_id = models.CharField(max_length=50, blank=True, null=True)


@receiver(post_save, sender=Notification)
def sendNotification(sender, instance, created, **kwargs):
    ids = [receiver.device_id for receiver in instance.receivers.all()]
    # pushNotification.apply_async((instance.message, ids, instance))
