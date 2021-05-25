from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.fields import related
from django.utils.functional import partition
from treebeard.mp_tree import MP_Node
from django.db.models.signals import post_save
from django.dispatch import receiver

from extendProfile.models import Profile

# Create your models here
from smileDesign.models import SmileDesignService


class ServiceCategory(MP_Node):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Service Category: %s' % self.name

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=30)
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=5)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=30)
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    doctor = models.ManyToManyField(
        Doctor,
        through='Service',
        through_fields=('related_patient', 'related_doctor'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return self.name


class Lab(models.Model):
    name = models.CharField(max_length=30)
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=5)

    def __str__(self):
        return str(self.name)

class Service(models.Model):
    related_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    related_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_design = models.ForeignKey(SmileDesignService, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Service #" + str(self.id)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    expected_date = models.DateTimeField(blank=True, null=True, default=datetime.today() + timedelta(days=60))
    actual_date = models.DateTimeField(blank=True, null=True, default=datetime.today() + timedelta(days=90))
    description = models.TextField(blank=True, null=True, max_length=500)
    STATUSES = (
        ('processing', 'Processing'),
        ('delayed', 'Delayed'),
        ('sent', 'Sent'),
        ('underdevelopment', 'Under Development'),
        ('finalized', 'Finalized'),
        ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="processing")
    finalized_lab = models.ForeignKey(Lab, on_delete=models.SET_NULL, blank=True, null=True)
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "Order #" + str(self.id)


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    expected_date = models.DateTimeField(blank=True, null=True)
    actual_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    STATUSES = (
        ('processing', 'Processing'),
        ('finalized', 'Finalized'),
        ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="processing")
    related_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    related_lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    reciept_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Invoice #" + str(self.id)



# PatientPic
class PatientPic(models.Model):
    smile_image = models.ImageField(blank=True, null=True)
    full_smile_image = models.ImageField(blank=True, null=True)
    side_image = models.ImageField(blank=True, null=True)
    optional_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patientPics")




@receiver(post_save, sender=Patient)
def create_patient_pic(sender, instance, created, **kwargs):
    if not created:
        pics = instance._patient_pics
        PatientPic(
            smile_image=pics['smile_image'], 
            full_smile_image=pics['full_smile_image'],
            side_image=pics['side_image'],
            optional_image=pics['optional_image'],
            patient=instance
        ).save()



@receiver(post_save, sender=Order)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        order = instance
        invoice = Invoice(
            related_service=order.related_service,
            expected_date=order.expected_date,
            actual_date=order.actual_date,
            description=order.description,
            related_order=order,
            related_lab=order.finalized_lab,
        )
        invoice.save()
        instance._invoice = invoice.id
        instance.save()







