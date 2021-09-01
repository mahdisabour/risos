from logging import info

from django.db.models.fields import related
from smileDesign.tasks import aiConnection
from smileDesign.models import SmileDesignService
from django.db.models import fields
from graphene.types import interface
from graphene.types.inputobjecttype import InputObjectType
from .models import BadColorReason, Doctor, Invoice, Lab, LabPic, Order, Patient, Service, Ticket, Tooth, ToothSevice
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
import base64
import json

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
        # kwargs['phone_number'] = str(randint(10**10, 10**11))
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

        doctor = Doctor.objects.get(
            related_profile=Profile.objects.get(id=kwargs["profile_doctor_id"]))

        patient = Patient.objects.get(related_profile=profile_obj)
        
        if kwargs["patient_pics"]:
            patient._patient_pics = kwargs["patient_pics"]
            smile_design = SmileDesignService(patient=patient, doctor=doctor)
            smile_design.save()
            patient._smile_design = smile_design
            patient.save()
        
        patient.doctor.add(doctor)
        return CreatePatient(user=user.id, profile=profile_obj.id, token=token, refresh_token=refresh_token)



class DeletePatient(graphene.Mutation):
    status = graphene.String()
    class Arguments:
        patient_id = graphene.Int(required=True)
        # doctor_id = graphene.Int(required=True)

    def mutate(self, info, patient_id):
        patient = Patient.objects.get(id=patient_id)
        # doctor = Doctor.objects.get(id=doctor_id)
        # patient.doctor.remove(doctor)
        # patient.save()
        patient.soft_delete()
        return DeletePatient(status="Success")
        



class UpdatePatientPic(graphene.Mutation):
    status = graphene.String()
    class Arguments:
        patient_pics = patientPics(required=True)
        patient_id = graphene.Int(required=True)
        doctor_id = graphene.Int(required=False)

    def mutate(self, info, patient_pics, patient_id, doctor_id):
        patient = Patient.objects.get(id=patient_id)
        patient._patient_pics = patient_pics
        if doctor_id:
            smile_design = SmileDesignService.objects.get(patient__id=patient_id, doctor__id=doctor_id)
            patient._smile_design = smile_design
        patient.save()
        return UpdatePatientPic(status="Success")


class patientPicsDeletion(graphene.InputObjectType):
    smile_image = graphene.Boolean(required=False)
    full_smile_image = graphene.Boolean(required=False)
    side_image = graphene.Boolean(required=False)
    optional_image = graphene.Boolean(required=False)


class DeletePatientPic(graphene.Mutation):
    status = graphene.String()
    class Arguments:
        patient_id = graphene.Int(required=True)
        selected_fields = patientPicsDeletion()

    def mutate(self, info, selected_fields, patient_id):    
        patient = Patient.objects.get(id=patient_id)
        patient_pic = patient.patient_pic
        print(selected_fields)
        for key, val in selected_fields.items():
            if val:
                setattr(patient_pic, key, None)

        patient_pic.save()
        return DeletePatientPic(status="Success")




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



# create Invoice
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceType(DjangoObjectType):
    class Meta:
        model = Invoice


class CreateInvoice(DjangoModelFormMutation):
    invoice = graphene.Field(InvoiceType)

    class Meta:
        form_class = InvoiceForm
        # exclude_fields = ("id", )






class UpdateOrder(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        order_id = graphene.ID(required=True)
        expected_date = graphene.DateTime()
        # actual_date = graphene.DateTime()
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



class TeethInput(graphene.InputObjectType):
    tooth_number = graphene.Int(required=True)
    tooth_service = graphene.String(required=False)
    cl = graphene.Int(required=False)


class ToothMutation(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        teeth = graphene.List(TeethInput)
        related_service = graphene.ID(required=True)


    def mutate(self, info, teeth, related_service):
        related_service = Service.objects.get(id=related_service)
        for tooth in teeth:
            tooth_service = None
            if "tooth_service" in tooth.keys():
                tooth_service = ToothSevice.objects.get(
                    name=tooth["tooth_service"])
            th = Tooth.objects.filter(
                tooth_number=tooth["tooth_number"],
                related_service=related_service
            )
            if th.exists():
                th = th.first()
                if tooth_service:
                    th.tooth_service = tooth_service
                th.save()
            else:
                tooth = Tooth(
                    tooth_number=tooth["tooth_number"],
                    related_service=related_service,
                    tooth_service=tooth_service,
                    cl=tooth["cl"]
                ).save()
        return ToothMutation(status="success")



class ToothMutationJson(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        json_object = graphene.JSONString(required=False)
        related_service = graphene.ID(required=True)
        central_size = graphene.String(required=False)

    def mutate(self, info, related_service, json_object, central_size):
        related_service = Service.objects.get(id=related_service)
        related_service.central_size = int(central_size)
        related_service.save()
        data = json_object
        for key, val in data.items():
            tooth_number = int(key)
            if Tooth.objects.filter(related_service=related_service, tooth_number=tooth_number).exists():
                tooth = Tooth.objects.get(related_service=related_service, tooth_number=tooth_number)
            else:
                tooth = Tooth(related_service=related_service, tooth_number=tooth_number)
            tooth_service = ToothSevice.objects.get(name=val["chosenService"])
            cl = val["cl"]
            tooth.tooth_service = tooth_service
            tooth.cl = cl
            tooth.save()
            return ToothMutationJson(status="Success")
        


class UpdateLabRate(graphene.Mutation):
    rate = graphene.Float()

    class Arguments:
        lab_id = graphene.Int(required=True)
        rate = graphene.Float(required=True)

    def mutate(self, info, lab_id, rate):
        lab = Lab.objects.get(id=lab_id)
        rate = (lab.rating * lab.rate_size + rate) / (lab.rate_size + 1)
        lab.rating = rate
        lab.rate_size = lab.rate_size + 1
        lab.save()
        return UpdateLabRate(rate=rate)


class CreateTicket(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        sender_profile = graphene.Int(required=True)
        receiver_profile = graphene.Int(required=True)
        message = graphene.String(required=True)
        related_order = graphene.Int(required=True)
    
    def mutate(self, info, sender_profile, receiver_profile, message, related_order):
        sender = Profile.objects.get(id=sender_profile)
        receiver = Profile.objects.get(id=receiver_profile)
        related_order = Order.objects.get(id=related_order)
        Ticket(
            sender=sender,
            receiver=receiver,
            related_order=related_order, 
            message=message
        ).save()
        return CreateTicket(status="Success")




class BusinessLogicMutations(graphene.ObjectType):
    create_lab = CreateLab.Field()
    create_patient = CreatePatient.Field()
    delete_patient = DeletePatient.Field()
    update_patient_pic = UpdatePatientPic.Field()
    delete_patient_pic = DeletePatientPic.Field()
    update_order = UpdateOrder.Field()
    create_order = CreateOrder.Field()
    create_invoice = CreateInvoice.Field()
    labpic_mutation = LabPicMutation.Field()
    update_lab_rate = UpdateLabRate.Field()
    create_service = CreateService.Field()
    tooth_mutation = ToothMutation.Field()
    tooth_mutation_json = ToothMutationJson.Field()
    create_ticker = CreateTicket.Field()


    
# search part
# this part should be here !!!!!!!!!!!!
class PatientType(DjangoObjectType):
    class Meta:
        model = Patient