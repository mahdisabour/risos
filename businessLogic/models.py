from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from treebeard.mp_tree import MP_Node

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
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
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
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.name


class Service(models.Model):
    related_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    related_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_design = models.ForeignKey(SmileDesignService, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Service #" + self.id


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    expected_date = models.DateTimeField(blank=True, null=True)
    actual_date = models.DateTimeField(blank=True, null=True)
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
        return "Order #" + self.id


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE)
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
    reciept_image = models.ImageField()

    def __str__(self):
        return "Invoice #" + self.id
