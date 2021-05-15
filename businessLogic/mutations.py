from .models import Doctor, Patient
from extendProfile.models import *
from extendProfile.mutations import CreateUser

import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from graphene import relay, ObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token
from graphene_file_upload.scalars import Upload




class CreatePatient(CreateUser):

    class Arguments:
        username = graphene.String(required=True)
        profile_doctor_id = graphene.Int(required=True)
        pic1 = graphene.

    def mutate(self, info, username, profile_doctor_id):
        user = get_user_model()(
            username=username,
            email="",
        )
        user.set_password(username)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        profile_obj.role = "patient"
        profile_obj.save()

        patinet = Patient.objects.get(related_profile=profile_obj)
        doctor = Doctor.objects.get(related_profile=Profile.objects.get(id=profile_doctor_id))
        patinet.doctor.add(doctor)
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)


class CreateLab(CreateUser):

    class Arguments:
        username = graphene.String(required=True)

    def mutate(self, info, username):
        user = get_user_model()(
            username=username,
            email="",
        )
        user.set_password(username)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        profile_obj.role = "lab"
        profile_obj.save()
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)





class BusinessLogicMutations(graphene.ObjectType):
    create_lab = CreateLab.Field()
    create_patient = CreatePatient.Field()
