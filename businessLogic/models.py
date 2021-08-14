from datetime import datetime, timedelta, timezone
from typing_extensions import IntVar
from notification.models import NotifReceiver, NotifService, Notification
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.fields import related
from django.utils.functional import partition
from treebeard.mp_tree import MP_Node
from django.db.models.signals import post_save
from django.dispatch import receiver
import base64
from graphene_file_upload.scalars import Upload
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO


from extendProfile.models import Profile

# Create your models here
from smileDesign.models import SmileDesignService
from django.core.validators import MinValueValidator, MaxValueValidator


from smileDesign.tasks import aiConnection, aiReady


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True

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
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rate_size = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return str(self.id)


class Patient(SoftDeleteModel):
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    doctor = models.ManyToManyField(
        Doctor,
        through='Service',
        through_fields=('related_patient', 'related_doctor'),
    )
    # patient_pic = models.OneToOneField("businessLogic.PatientPic", on_delete=models.CASCADE, blank=True, null=True, related_name="patient")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return str(self.related_profile.phone_number)


class Lab(models.Model):
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rate_size = models.IntegerField(default=0)

    def __str__(self):
        return str(self.related_profile.first_name)

class Service(models.Model):
    related_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="services")
    related_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_design = models.ForeignKey(SmileDesignService, blank=True, null=True, on_delete=models.CASCADE)
    central_size = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Service #" + str(self.id)


class ToothSevice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class BadColorReason(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class Tooth(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    tooth_number = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(48)])
    tooth_service = models.ForeignKey(ToothSevice, on_delete=models.CASCADE, blank=True, null=True)
    cl = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    is_bad_color = models.BooleanField(default=False)
    bad_color_reason = models.ForeignKey(BadColorReason, on_delete=models.CASCADE, blank=True, null=True)
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="Teeth")

    def __str__(self):
        return self.tooth_service.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    expected_date = models.DateTimeField(blank=True, null=True, default=datetime.today() + timedelta(days=60))
    # should be checked
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
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")

    def __str__(self):
        return "Order #" + str(self.id)


class Invoice(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    # should be checked
    expected_date = models.DateTimeField(blank=True, null=True)
    actual_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    STATUSES = (
        ('processing', 'Processing'),
        ('finalized', 'Finalized'),
        ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="processing")
    related_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices")
    related_lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    reciept_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Invoice #" + str(self.id)



# PatientPic
class PatientPic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', blank=True, null=True)
    smile_image = models.ImageField(blank=True, null=True)
    full_smile_image = models.ImageField(blank=True, null=True)
    side_image = models.ImageField(blank=True, null=True)
    optional_image = models.ImageField(blank=True, null=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, blank=True, null=True, related_name="patient_pic")


class LabPic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at', blank=True, null=True)
    pic = models.ImageField(blank=True, null=True, upload_to="labpics/")
    lab = models.OneToOneField(Lab, on_delete=models.CASCADE, related_name="labPics")
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True)

    class Meta:
        unique_together = ('lab', 'number', )

    def __str__(self):
        return f"{self.lab.related_profile.first_name}: pic #{self.id}"



@receiver(post_save, sender=Patient)
def create_patient_pic(sender, instance, created, **kwargs):
    print("patient created")
    if not created:
        try:
            pics = instance._patient_pics
            patient_pic = PatientPic(
                patient=instance
            )
            for key, val in pics.items():
                if val:
                    if (isinstance(val, InMemoryUploadedFile)):
                        setattr(patient_pic, key, val)
                    else:
                        data = base64.b64decode(val)
                        new_path = f"{key}_{instance.id}_{datetime.now()}.png"
                        image_path = f"./mediafiles/{new_path}"
                        with open(image_path, "wb") as f:
                            f.write(data)
                        setattr(patient_pic, key, new_path)
            try:
                patient_pic._smile_design = instance._smile_design
            except:
                pass
            patient_pic.save()
        except:
            pass
        


@receiver(post_save, sender=PatientPic)
def update_patient_pics(sender, instance, created, **kwargs):
    print("patient pic created")
    patient = instance.patient
    try:
        smile_design = instance._smile_design
        smile_image = instance.smile_image
        image_url = smile_image.url
        # ai_response = aiConnection.apply_async((image_url, ))
        aiConnection.apply_async((image_url, ), link=aiReady.s(smile_design.id, patient.id) )
    except:
        pass
        # smile_design = SmileDesignService()
        # smile_design.save()

    


@receiver(post_save, sender=Order)
def notif_base_on_order(sender, instance, created, **kwargs):
    print("order signal")
    patient_fname = instance.related_service.related_patient.related_profile.first_name
    # patient_lname = instance.related_service.related_patient.related_profile.last_name
    if created:
        message = f"order completed - {patient_fname}"
    else:
        message = f"order updated - {patient_fname}"
    # patinet_profile = instance.related_service.related_patient
    lab_profile = None
    try:
        doctor_profile = instance.related_service.related_doctor.related_profile
        lab_profile = instance.finalized_lab.related_profile
    except:
        pass
    profiles = [doctor_profile, lab_profile]
    receivers = [NotifReceiver.objects.filter(profile=profile).first() for profile in profiles if profile]
    if NotifService.objects.filter(object_id=instance.id, object_type="order").exists():
        notif_service = NotifService.objects.get(object_id=instance.id, object_type="order")
    else:
        notif_service = NotifService(object_id=instance.id, object_type="order")
        notif_service.save()
    notif = Notification(
        message=message, 
        notif_service=notif_service,
    )
    notif.save()
    notif.receivers.set(receivers)
    notif.save()
        


