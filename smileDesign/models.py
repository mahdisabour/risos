from django.db import models
from treebeard.mp_tree import MP_Node
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save


class SmileCategory(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Smile Category: %s' % self.name

    def __str__(self):
        return self.name


class SmileColor(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Smile Color: %s' % self.name

    def __str__(self):
        return self.name


class FaceShape(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return self.name


class SmileDesignService(models.Model):
    teeth_less_image = models.ImageField(blank=True, null=True)
    smile_image_result = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_color = models.ForeignKey(
        SmileColor, on_delete=models.CASCADE, blank=True, null=True)
    related_smile_category = models.ForeignKey(
        SmileCategory, on_delete=models.CASCADE, blank=True, null=True)
    patient = models.ForeignKey("businessLogic.Patient", on_delete=models.CASCADE,
                                blank=True, null=True, related_name="smile_designs")
    doctor = models.ForeignKey("businessLogic.Doctor", on_delete=models.CASCADE,
                               blank=True, null=True, related_name="smile_designs")
    STATUSES = (
        ("ready", "READY"),
        ("notready", "NOTREADY"),
        ("improper image", "IMPROPER IMAGE")
    )
    status = models.CharField(
        max_length=20, choices=STATUSES, default="notready")
    shape = models.ForeignKey(
        FaceShape, on_delete=models.CASCADE, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    heigth = models.IntegerField(blank=True, null=True)


    class Meta:
        unique_together = ('doctor', 'patient', )

    def __str__(self):
        return str(self.id)
