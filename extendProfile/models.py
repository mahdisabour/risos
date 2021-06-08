import businessLogic.models as bModels
from random import randint

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxLengthValidator

from extendProfile.smshelper import otp_send

from .tasks import disableOTP



active_roles = (
    ("doctor", "Doctor"),
    ("patient", "Patient"),
    ("lab", "Lab")
)


def random_with_N_digits():
    n = settings.OTP_NUMBER_OF_DIGITS
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return str(randint(range_start, range_end))


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=120, choices=active_roles, default="doctor")
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile/', blank=True, null=True)
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    )
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    age = models.IntegerField(validators=[MaxLengthValidator(100)], blank=True, null=True)
    STATUSES = (
        ('active', 'Active'),
        ('deactive', 'Deactive'),
        ('freetrial', 'Freetrial'),
        ('banned', 'Banned')
    )
    status = models.CharField(max_length=10, choices=STATUSES, default="freetrial")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    email = models.EmailField(max_length=40, blank=True, null=True)

    # def __str__(self):
    #     return self.phone_number


class OTP(models.Model):
    message = models.CharField(max_length=7, default=random_with_N_digits, blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username}"

@receiver(post_save, sender=OTP)
def otp_time_arrive(sender, instance, *args, **kwargs):
    print("teeeeeeeeeeeeeeeeeeeeeeeeeeest")
    disableOTP.apply_async((instance.id, ), countdown=120)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.phone_number = instance.username
        profile.email = instance.email
        profile.save()


@receiver(post_save, sender=Profile)
def create_sub_user(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'doctor':
            bModels.Doctor(related_profile=instance).save()
    
    if instance.role == 'patient':
        if not bModels.Patient.objects.filter(related_profile=instance).exists():
            bModels.Patient(related_profile=instance).save()

    if instance.role == 'lab':
        if not bModels.Lab.objects.filter(related_profile=instance).exists():
            bModels.Lab(related_profile=instance).save()




@receiver(post_save, sender=Profile)
def create_profile_otp(sender, instance, created, **kwargs):
    if created:
        otp_s = OTP.objects.create(profile=instance)
        otp_s.save()
        # wallet = Wallet.objects.create(related_profile=instance, amount=0)
        # wallet.save()
        instance.save()


@receiver(post_save, sender=OTP)
def send_otp(sender, instance, created, **kwargs):
    if created:
        phone_number = instance.profile.user.username
        otp_send(phone_number, instance.message)



