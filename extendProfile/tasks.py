from risos.celery import app
from django.conf import settings
import extendProfile.models as eModels 


@app.task
def disableOTP(*args):
    instance = eModels.OTP.objects.get(id = args[0])
    instance.is_valid = False
    instance.save()