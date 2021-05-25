from risos.celery import app
from django.conf import settings



@app.task
def disableOTP(self, instance):
    instance.is_valid = False
    instance.save()