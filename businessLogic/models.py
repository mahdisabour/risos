from datetime import datetime, timedelta
from notification.models import NotifReceiver, NotifService, Notification
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from treebeard.mp_tree import MP_Node
from django.db.models.signals import post_save
from django.dispatch import receiver
import base64
from graphene_file_upload.scalars import Upload
from django.core.files.uploadedfile import InMemoryUploadedFile
from extendProfile.models import Profile
from smileDesign.models import SmileDesignService
from django.core.validators import MinValueValidator, MaxValueValidator
from smileDesign.tasks import aiConnection, aiReady


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)
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
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    node_order_by = ['name']

    def __unicode__(self):
        return 'Service Category: %s' % self.name

    def __str__(self):
        return self.name


class Doctor(models.Model):
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rate_size = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return str(self.id)


class Patient(SoftDeleteModel):
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    doctor = models.ManyToManyField(
        Doctor,
        # through='Service',
        # through_fields=('related_patient', 'related_doctor'),
    )
    patient_pic = models.OneToOneField("businessLogic.PatientPic", on_delete=models.CASCADE, blank=True, null=True, related_name="patient")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return str(self.related_profile.phone_number)


class Lab(models.Model):
    related_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rate_size = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Service(models.Model):
    related_doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="services")
    related_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    related_smile_design = models.ForeignKey(
        SmileDesignService, blank=True, null=True, on_delete=models.CASCADE)
    central_size = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Service #" + str(self.id)


class ToothSevice(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BadColorReason(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tooth(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    tooth_number = models.PositiveIntegerField(
        validators=[MinValueValidator(11), MaxValueValidator(48)])
    tooth_service = models.ForeignKey(
        ToothSevice, on_delete=models.CASCADE, blank=True, null=True)
    cl = models.PositiveIntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(100)], blank=True, null=True)
    is_bad_color = models.BooleanField(default=False)
    bad_color_reason = models.ForeignKey(
        BadColorReason, on_delete=models.CASCADE, blank=True, null=True)
    related_service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="Teeth")

    def __str__(self):
        return self.tooth_service.name


class Order(models.Model):
    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__prev_status__ = self.status
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateField(auto_now=True, verbose_name='Updated at')
    expected_date = models.DateField(
        blank=True, null=True, default=datetime.today() + timedelta(days=60))
    description = models.TextField(blank=True, null=True, max_length=500)
    STATUSES = (
        ('sent', 'Sent'),
        ('processing_invoice ready', 'Invoice Ready'),
        ('processing_accept', 'Accept'),
        ('processing_reject', 'Reject'),
        ('processing_reject and resend', 'Reject And Resend'),
        ('processing_molding', 'Molding'),
        ('processing_ditch', 'Ditch'),
        ('processing_scan', 'Scan'),
        ('processing_water wax', 'Water Wax'),
        ('processing_designing', 'Designing'),
        ('processing_print/milling', 'Print/Milling'),
        ('processing_ceramic', 'Ceramic'),
        ('ready', 'ready')
    )
    status = models.CharField(
        max_length=30, choices=STATUSES, default="sent")
    finalized_lab = models.ForeignKey(
        Lab, on_delete=models.SET_NULL, blank=True, null=True)
    related_service = models.ForeignKey(
        Service, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")

    def __str__(self):
        return "Order #" + str(self.id)



class Invoice(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    actual_date = models.DateField(
        blank=True, null=True, default=datetime.today() + timedelta(days=90))
    price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    related_order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="invoice")
    reciept_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Invoice #" + str(self.id)


class PatientPic(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at', blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Updated at', blank=True, null=True)
    smile_image = models.ImageField(blank=True, null=True)
    full_smile_image = models.ImageField(blank=True, null=True)
    side_image = models.ImageField(blank=True, null=True)
    optional_image = models.ImageField(blank=True, null=True)
    # patient = models.OneToOneField(
    #     Patient, on_delete=models.CASCADE, blank=True, null=True, related_name="patient_pic")


class Log(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at', blank=True, null=True)
    related_order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="logs")
    status = models.CharField(max_length=50)
    message = models.CharField(max_length=250, blank=True, null=True)


class Ticket(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    message = models.CharField(max_length=50)
    related_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    STATUS = (
        ('read', 'Read'),
        ('unread', 'Unread'),
    )
    messgae_status = models.CharField(choices=STATUS, max_length=50, default='unread')


class LabPic(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at', blank=True, null=True)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Updated at', blank=True, null=True)
    pic = models.ImageField(blank=True, null=True, upload_to="labpics/")
    lab = models.OneToOneField(
        Lab, on_delete=models.CASCADE, related_name="labPics")
    number = models.IntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(6)], blank=True, null=True)

    class Meta:
        unique_together = ('lab', 'number', )

    def __str__(self):
        return f"{self.lab.related_profile.first_name}: pic #{self.id}"


@receiver(post_save, sender=Patient)
def create_patient_pic(sender, instance, created, **kwargs):
    if not created:
        try:
            pics = instance._patient_pics
            if PatientPic.objects.filter(patient=instance):
                patient_pic = PatientPic.objects.get(patient=instance)
            else:
                patient_pic = PatientPic(
                    patient=instance
                )
            for key, val in pics.items():
                if val:
                    if (isinstance(val, InMemoryUploadedFile)):
                        print(key, val)
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
        smile_design.status = "notready"
        smile_design.save()
        smile_image = instance.smile_image
        image_url = smile_image.url
        aiConnection.apply_async(
            (image_url, smile_design.id), link=aiReady.s(smile_design.id, patient.id))
    except:
        pass


@receiver(post_save, sender=Invoice)
def _post_save_receiver(sender, instance, created, **kwargs):
    instance.related_order.status = "processing_invoice ready"
    instance.related_order.save()


@receiver(post_save, sender=Order)
def notif_base_on_order(sender, instance, created, **kwargs):
    # save log
    print(instance.__prev_status__)
    print(instance.status)
    if instance.status != instance.__prev_status__:
        order_id = instance.id
        status = instance.status
        message = f"سفارش {order_id} به {status} تغییر وضعیت یافت "
        Log(related_order=instance, status=instance.status, message=message).save()
    # notif handler
    patient_fname = instance.related_service.related_patient.related_profile.first_name
    if created:
        message = f"order registered - {patient_fname}"
    else:
        message = f"order updated - {patient_fname}"

    lab_profile = None
    try:
        doctor_profile = instance.related_service.related_doctor.related_profile
        lab_profile = instance.finalized_lab.related_profile
    except:
        pass
    profiles = [doctor_profile, lab_profile]
    # receivers = [NotifReceiver.objects.filter(profile=profile).first() for profile in profiles if profile]
    receivers = []
    if NotifService.objects.filter(object_id=instance.id, object_type="order").exists():
        notif_service = NotifService.objects.get(
            object_id=instance.id, object_type="order")
    else:
        notif_service = NotifService(
            object_id=instance.id, object_type="order")
        notif_service.save()
    notif = Notification(
        message=message,
        notif_service=notif_service,
    )
    notif.save()
    notif.receivers.set(receivers)
    notif.save()
