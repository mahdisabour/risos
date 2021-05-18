from graphene.types.inputobjecttype import InputObjectType
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



class patientPics(graphene.InputObjectType):
    smile_image = Upload(required=False)
    full_smile_image = Upload(required=False)
    side_image = Upload(required=False)
    optional_image = Upload(required=False)



class CreatePatient(CreateUser):

    class Arguments:
        username = graphene.String(required=True)
        profile_doctor_id = graphene.Int(required=True)
        profile_pic = Upload(required=False)
        patient_pics = patientPics(required=False)

    def mutate(self, info, username, profile_doctor_id, profile_pic, patient_pics):
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
        try:
            # profile_obj.profile_pic.save(f'user:{profile_obj.role}.png', open(image_url, 'rb'))
            profile_obj.profile_pic = profile_pic
            profile_obj.save()
        except Exception as e:
            profile_obj.save()
            print(e)

        # assign some attr to patient to create order when patient create
        patient = Patient.objects.get(related_profile=profile_obj)
        if patient_pics:
            patient._patient_pics = patient_pics
            patient.save()

        doctor = Doctor.objects.get(related_profile=Profile.objects.get(id=profile_doctor_id))
        patient.doctor.add(doctor)
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)


class CreateLab(CreateUser):

    class Arguments:
        username = graphene.String(required=True)
        profile_pic = Upload(required=False)

    def mutate(self, info, username, profile_pic):
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
        try:
            # profile_obj.profile_pic.save(f'user:{profile_obj.role}.png', open(image_url, 'rb'))
            profile_obj.profile_pic = profile_pic
            profile_obj.save()
        except Exception as e:
            profile_obj.save()
            print(e)
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)





class BusinessLogicMutations(graphene.ObjectType):
    create_lab = CreateLab.Field()
    create_patient = CreatePatient.Field()
