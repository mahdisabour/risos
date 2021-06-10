from inspect import Arguments
from .models import *
import graphene
from django.conf import settings
from django.contrib.auth.models import User

class CreateDevice(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)
        device_id = graphene.String(required=True)

    def mutate(self, info, user_id, device_id):
        user = User.objects.get(id = user_id)
        Receiver(
            device_id=device_id,
            user = user
        ).save()
        return CreateDevice(status="Success")


class NotificationMutations(graphene.ObjectType):
    create_device = CreateDevice.Field()