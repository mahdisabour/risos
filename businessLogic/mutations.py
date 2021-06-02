from django.db.models import fields
from graphene.types.inputobjecttype import InputObjectType
from .models import Doctor, Invoice, Lab, LabPic, Order, Patient, Service, create_invoice
from extendProfile.models import *
from extendProfile.mutations import CreateUser, UpdateProfile

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

from django.core.files import File

from extendProfile.mutations import ProfileInput




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

        doctor = Doctor.objects.get(related_profile=Profile.objects.get(id=kwargs["profile_doctor_id"]))
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


# class CreateOrder(graphene.Mutation):
#     order = graphene.Field(String)
#     invoice = graphene.Field(String)
    
#     class Arguments:
#         finalized_lab_id = graphene.Int()
#         related_service_id = graphene.Int()
#         expected_date = graphene.DateTime()
#         actual_date = graphene.DateTime()

#     def mutate(self, 
#                info, 
#                finalized_lab_id, 
#                related_service_id, 
#                expected_date, 
#                actual_date):
#         lab = Lab.objects.get(id=finalized_lab_id)
#         service = None
#         try:
#             service = Service.objects.get(id=related_service_id)
#         except:
#             pass
#         order = Order(
#             expected_date=expected_date,
#             actual_date=actual_date,
#             finalized_lab=lab,
#             related_service=service
#         )
#         order.save()
#         return CreateOrder(order=order.id, invoice=order._invoice)




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

class OrderMutation(DjangoModelFormMutation):
    service = graphene.Field(OrderType)

    class Meta:
        form_class = OrderForm 



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



class InvoiceInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    updated_at = graphene.DateTime(required=False)
    related_service = graphene.Int(required=False)
    expected_date = graphene.DateTime(required=False)
    actual_date = graphene.DateTime(required=False)
    description = graphene.String(required=False)
    status = graphene.String(required=False)
    related_order = graphene.Int(required=False)
    related_lab = graphene.Int(required=False)
    reciept_image = Upload(required=False)

class UpdateInvoice(graphene.Mutation):
    status = graphene.String()
    class Arguments:
        invoice_data = InvoiceInput()
    def mutate(self, info, invoice_data=None):
        invoice = Invoice.objects.get(id=invoice_data.id)
        for k, v in invoice_data.items():
            setattr(invoice, k, v)
        invoice.save()
        return UpdateInvoice(status="success")



class LabPicInput(graphene.InputObjectType):
    lab_id = graphene.ID(required=True)
    pic1 = Upload(required=False)
    pic2 = Upload(required=False)
    pic3 = Upload(required=False)
    pic4 = Upload(required=False)
    pic5 = Upload(required=False)
    pic6 = Upload(required=False)

class LabPicMutation(graphene.Mutation):
    status = graphene.String()
    class Arguments:
        labpic_data = LabPicInput()
    def mutate(seld, info, labpic_data=None):
        if (LabPic.objects.filter(lab=Lab.objects.get(id=labpic_data.lab_id)).exists()):
            lab_pic = LabPic.objects.get(lab=Lab.objects.get(id=labpic_data.lab_id)) 
        else :
            lab_pic = LabPic(lab=Lab.objects.get(id=labpic_data.lab_id))
        
        for k, v in labpic_data.items():
            setattr(labpic_data, k, v)
        lab_pic.save()
        return LabPicMutation(status="success")
        



class BusinessLogicMutations(graphene.ObjectType):
    create_lab = CreateLab.Field()
    create_patient = CreatePatient.Field()
    # create_order = CreateOrder.Field()
    order_mutation = OrderMutation.Field()
    update_invoice = UpdateInvoice.Field()
    labpic_mutation = LabPicMutation.Field()
    create_service = CreateService.Field()
