from inspect import Arguments
from .models import *
import graphene
from django.conf import settings
from django.contrib.auth.models import User
from graphql_jwt.utils import get_payload
from graphql_jwt.decorators import login_required



class CreateDevice(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        user_id = graphene.ID(required=True)
        device_id = graphene.String(required=True)


    def mutate(self, info, user_id, device_id):
        # user = info.context.user
        # token = info.context.META.get("HTTP_TOKEN")
        # print(get_payload(token, info.context))
        # print(token)

        user = User.objects.get(id = user_id)
        Receiver(
            device_id=device_id,
            user = user
        ).save()
        return CreateDevice(status="Success")


class NotificationMutations(graphene.ObjectType):
    create_device = CreateDevice.Field()