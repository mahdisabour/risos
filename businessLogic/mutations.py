from django.db.models import fields
from graphene.types import interface
from graphene.types.inputobjecttype import InputObjectType
from .models import BadColorReason, Doctor, Invoice, Lab, LabPic, Order, Patient, Service, Tooth, ToothSevice
from extendProfile.models import *
from extendProfile.mutations import CreateUser, UpdateProfile
from django.db.models import Q

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
from graphene_django.forms.mutation import DjangoModelFormMutation
from django import forms
import django_filters
import requests

from django.core.files import File


class patientPics(graphene.InputObjectType):
    smile_image = Upload(required=False)
    full_smile_image = Upload(required=False)
    side_image = Upload(required=False)
    optional_image = Upload(required=False)


class CreatePatient(CreateUser):
    class Arguments:
        patient_pics = patientPics(required=False)
        phone_number = graphene.String(required=True)
        name = graphene.String(required=False)
        age = graphene.Int(required=False)
        email = graphene.String(required=False, default_value="")
        address = graphene.String(required=False)
        description = graphene.String(required=False)
        profile_doctor_id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        user = get_user_model()(
            username=kwargs['phone_number'],
            email=kwargs['email'],
        )
        user.set_password(kwargs['phone_number'])
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        profile_obj.role = "patient"
        profile_obj.first_name = kwargs["name"]
        profile_obj.age = kwargs["age"]
        profile_obj.email = kwargs["email"]
        profile_obj.address = kwargs["address"]
        profile_obj.description = kwargs["description"]
        profile_obj.save()

        patient = Patient.objects.get(related_profile=profile_obj)
        if kwargs["patient_pics"]:
            patient._patient_pics = kwargs["patient_pics"]
            patient.save()

        doctor = Doctor.objects.get(
            related_profile=Profile.objects.get(id=kwargs["profile_doctor_id"]))
        patient.doctor.add(doctor)
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)


class CreateLab(CreateUser):
    class Arguments:
        phone_number = graphene.String(required=True)
        name = graphene.String(required=False)
        telephone_number = graphene.String(required=False)
        address = graphene.String(required=False)
        description = graphene.String(required=False)

    def mutate(self, info, **kwargs):
        user = get_user_model()(
            username=kwargs["phone_number"],
            email="",
        )
        user.set_password(kwargs["phone_number"])
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        profile_obj.role = "lab"
        profile_obj.first_name = kwargs["name"]
        profile_obj.telephone_number = kwargs["telephone_number"]
        profile_obj.address = kwargs["address"]
        profile_obj.description = kwargs["description"]
        profile_obj.save()
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)


# create order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class CreateOrder(DjangoModelFormMutation):
    service = graphene.Field(OrderType)

    class Meta:
        form_class = OrderForm
        exclude_fields = ("id", )


class UpdateOrder(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        order_id = graphene.ID(required=True)
        expected_date = graphene.DateTime()
        actual_date = graphene.DateTime()
        description = graphene.String()
        status = graphene.String()
        finalized_lab = graphene.ID()
        related_service = graphene.ID()

    def mutate(self, info, **kwargs):
        order = Order.objects.get(id=kwargs["order_id"])
        lab = None
        service = None
        if kwargs["finalized_lab"]:
            lab = Lab.objects.get(id=kwargs["finalized_lab"])
        if kwargs["related_service"]:
            service = Service.objects.get(id=kwargs["related_service"])
        kwargs["finalized_lab"] = lab
        kwargs["related_service"] = service
        for k, v in kwargs.items():
            if kwargs[k]:
                setattr(order, k, v)
        order.save()
        return UpdateOrder(status="success")


# create service
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service


class CreateService(DjangoModelFormMutation):
    service = graphene.Field(ServiceType)

    class Meta:
        form_class = ServiceForm
        exclude_fields = ("id", )


class LabPicMutation(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        pic_number = graphene.Int(required=True)
        lab_id = graphene.ID(required=True)
        pic = Upload(required=True)

    def mutate(self, info, pic_number, lab_id, pic):
        lab = Lab.objects.get(id=lab_id)
        lab_pic = LabPic.objects.filter(number=pic_number, lab=lab)
        if lab_pic.exists():
            lab_pic = lab_pic.first()
            lab_pic.pic = pic
            lab_pic.save()
        else:
            LabPic(lab=lab, pic=pic, number=pic_number).save()
        return LabPicMutation(status="success")


class ToothMutation(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        tooth_number = graphene.Int(required=True)
        related_service = graphene.ID(required=True)
        is_bad_color = graphene.Boolean(required=False)
        tooth_service = graphene.String(required=False)
        bad_color_reason = graphene.String(required=False)

    def mutate(self, info, **kwargs):
        related_service = Service.objects.get(id=kwargs["related_service"])
        tooth_service = None
        bad_color_reason = None
        if kwargs["tooth_service"]:
            tooth_service = ToothSevice.objects.get(
                name=kwargs["tooth_service"])
        if kwargs["bad_color_reason"]:
            bad_color_reason = BadColorReason.objects.get(
                name=kwargs["bad_color_reason"])
        tooth = Tooth.objects.filter(
            tooth_number=kwargs["tooth_number"],
            related_service=related_service
        )
        if tooth.exists():
            tooth = tooth.first()
            if kwargs["is_bad_color"]:
                tooth.is_bad_color = kwargs["is_bad_color"]
            if tooth_service:
                tooth.tooth_service = tooth_service
            if bad_color_reason:
                tooth.bad_color_reason = bad_color_reason
            tooth.save()
        else:
            tooth = Tooth(
                tooth_number=kwargs["tooth_number"],
                related_service=related_service,
                is_bad_color=kwargs["is_bad_color"],
                tooth_service=tooth_service,
                bad_color_reason=bad_color_reason
            ).save()
        return ToothMutation(status="success")



# search part
# bugggggggggg
class PatientType(DjangoObjectType):
    class Meta:
        model = Patient

class FilterPatient(graphene.ObjectType):
    filtered_patients = graphene.List(PatientType, name=graphene.String(
        required=True), doctor_id=graphene.ID(required=True))

    def resolve_filtered_patients(self, info, name, doctor_id):
        filtered_patients = Patient.objects.filter(
            (Q(related_profile__first_name__icontains=name) |
             Q(related_profile__last_name__icontains=name)) &
            Q(doctor__id=doctor_id)
        )
        return filtered_patients.all()


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class FilterOrderByPatient(graphene.ObjectType):
    filtered_orders = graphene.List(OrderType, name=graphene.String(
        required=True), doctor_id=graphene.ID(required=True))


    def resolve_filtered_orders(self, info, name, doctor_id):
        filtered_orders = Order.objects.filter(
            (Q(related_service__related_patient__related_profile__first_name=name) |
             Q(related_service__related_patient__related_profile__last_name=name)) &
            Q(related_service__related_doctor__id=doctor_id)
        )
        return filtered_orders.all()



class BusinessLogicMutations(graphene.ObjectType):
    create_lab = CreateLab.Field()
    create_patient = CreatePatient.Field()
    update_order = UpdateOrder.Field()
    create_order = CreateOrder.Field()
    labpic_mutation = LabPicMutation.Field()
    create_service = CreateService.Field()
    tooth_mutation = ToothMutation.Field()


    