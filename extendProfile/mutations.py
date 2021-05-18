from businessLogic.models import Doctor, Patient
import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene import relay, ObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token
from .models import *
from graphene_file_upload.scalars import Upload


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
# class UserMutationNode(DjangoObjectType):
#     class Meta:
#         model = get_user_model()
#         filter_fields = ['id']
#         interfaces = (relay.Node,)
#
#
# class ProfileMutationNode(DjangoObjectType):
#     class Meta:
#         model = Profile
#         filter_fields = ['id', 'phone_number', 'user']
#         interfaces = (relay.Node,)
#
#
# class BaseQuery(graphene.ObjectType):
#     user_mutation = relay.Node.Field(UserMutationNode)
#     all_users_muatition = DjangoFilterConnectionField(UserMutationNode)
#     profile_mutation= relay.Node.Field(ProfileMutationNode)
#     all_profiles_mutation = DjangoFilterConnectionField(ProfileMutationNode)


# Mutations --------------------
# -------------------------------
class RequestOTP(graphene.Mutation):
    status = graphene.Field(String)

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        user_obj = User.objects.get(username=username)
        profile_obj = Profile.objects.get(user=user_obj.id)
        otp = OTP(profile=profile_obj)
        otp.save()
        return RequestOTP(status="success")


class VerifyUser(graphene.Mutation):
    status = graphene.Field(String)

    class Arguments:
        username = graphene.String(required=True)
        otp_message = graphene.String(required=True)

    def mutate(self, info, username, otp_message):
        user_obj = User.objects.get(username=username)
        profile_obj = Profile.objects.get(user=user_obj.id)
        related_otp = OTP.objects.filter(profile=profile_obj.id)
        for otp in related_otp:
            if otp.message == otp_message and otp.is_valid == True:
                otp.valid = False
                profile_obj.status = True
                otp.save()
                profile_obj.save()
                return VerifyUser(status="success")
        return VerifyUser(status="failed")


# CreateUser
class CreateUser(graphene.Mutation):
    user = graphene.String()
    profile = graphene.String()
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        profile_pic = Upload(required=False)

    def mutate(self, info, username, password, profile_pic):
        user = get_user_model()(
            username=username,
            email="",
        )
        user.set_password(password)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        # save profile picture
        try:
            profile_obj.profile_pic = profile_pic
            profile_obj.save()
        except Exception as e:
            profile_obj.save()
            print(e)
        # phone_number = profile_obj.phone_number
        # otp = OTP.objects.get(profile=profile_obj.id)
        # otp_send(phone_number, otp.message)
        return CreateUser(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)




class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    profile = graphene.String()

    # ip = graphene.String()
    # session = graphene.String()

    # @classmethod
    # def Field(cls, *args, **kwargs):
    #     cls._meta.arguments.update({
    #         'session': graphene.String()
    #     })
    #     return super().Field(*args, **kwargs)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        # request = info.context.request
        # client_ip, is_routable = get_client_ip(request)
        # session = kwargs['session']
        profile = Profile.objects.filter(user=info.context.user).first()
        return cls(profile=profile.id)


class BaseMutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    verify_user = VerifyUser.Field()
    request_otp = RequestOTP.Field()



# schema = graphene.Schema(mutation=BaseMutation)