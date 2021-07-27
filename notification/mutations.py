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
        Profile_id = graphene.ID(required=True)
        device_id = graphene.String(required=True)


    def mutate(self, info, Profile_id, device_id):
        user = info.context.user
        print(user.id)
        # token = info.context.META.get("HTTP_TOKEN")
        # print(get_payload(token, info.context))
        # print(token)

        profile = Profile.objects.get(id = Profile_id)
        NotifReceiver(
            device_id=device_id,
            profile = profile
        ).save()
        return CreateDevice(status="Success")


class NotificationMutations(graphene.ObjectType):
    create_device = CreateDevice.Field()