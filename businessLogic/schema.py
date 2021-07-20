import django
from django.apps import apps
# from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
import django_filters
from django.db.models import ImageField, CharField
from graphene import relay, ObjectType, Schema, Field, Int
from graphene.types import field, interface
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
import graphene
from .models import *


def id_resolver(self, *_):
    return self.id

exempted_field_types = (GenericForeignKey, ImageField)
exempted_field_names = ('_field_status',)

def generate_filter_fields(model):
    # May want to add special string methods here eg istartswith
    return {f.name: ['in'] for f in model._meta.get_fields()
            if not isinstance(f, exempted_field_types) and f.name not in exempted_field_names}



class PlainTextNode(relay.Node):
    class Meta:
        name = 'businessLogicService'

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def from_global_id(global_id):
        return global_id.split(':')


class DoctorNode(DjangoObjectType):
    class Meta:
        model = Doctor
        filter_fields = generate_filter_fields(Doctor)
        interfaces = (PlainTextNode, )
        filter_order_by=True
    _id=Int(name='_id')
    resolve__id=id_resolver


class PatientNode(DjangoObjectType):
    class Meta:
        model = Patient
        filter_fields = generate_filter_fields(Patient)
        interfaces = (PlainTextNode, )
        filter_order_by = True
    _id=Int(name='_id')
    resolve__id=id_resolver


class PatientFilter(django_filters.FilterSet):
    filter_patient = django_filters.CharFilter(field_name="related_profile__first_name", lookup_expr='icontains')

    class Meta:
        model = Patient
        fields = []


class BusinessLogicQueryCustom(ObjectType):
    doctor = PlainTextNode.Field(DoctorNode)
    all_doctor = DjangoFilterConnectionField(DoctorNode)

    patient = PlainTextNode.Field(PatientNode)
    all_patient = DjangoFilterConnectionField(PatientNode, filterset_class=PatientFilter)





# custome query
custom_models = ["Doctor", "Patient"]


# Set this to your Django application name
# auto generate query 
APPLICATION_NAME = 'businessLogic'

class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass


def create_model_object_meta(model):
    return type('Meta',
                (object,),
                dict(model=model,
                     interfaces=(PlainTextNode,),
                     filter_fields=generate_filter_fields(model),
                     filter_order_by=True,
                     )
                )


def create_model_in_filters(model):
    model_name = model.__name__
    in_filters = {
        '{name}__in'.format(name=f.name): InFilter(field_name=f.name, lookup_expr='in')
        for f in model._meta.get_fields()
        if not isinstance(f, exempted_field_types) and f.name not in exempted_field_names}

    search_filters = {
        '{name}__search'.format(name=f.name): django_filters.CharFilter(field_name=f.name, lookup_expr='icontains')
        for f in model._meta.get_fields()
        if not isinstance(f, exempted_field_types) and f.name not in exempted_field_names and isinstance(f, CharField)}

    custome_filter = {}
    if model_name == "Lab":
        custome_filter = {'search_by_name': django_filters.CharFilter(
            field_name='related_profile__first_name', lookup_expr='icontains')}

    if model_name == "Order":
        custome_filter = {'search_by_name': django_filters.CharFilter(
            field_name='related_service__related_patient__related_profile__first_name', lookup_expr='icontains')}

    in_filters.update(search_filters)
    in_filters.update(custome_filter)

    fields = [f.name
              for f in model._meta.get_fields()
              if not isinstance(f, exempted_field_types) and f.name not in exempted_field_names]

    filter_class = type(
        '{model_name}InFilters'.format(model_name=model_name),
        (django_filters.FilterSet,),
        dict(
            in_filters,
            Meta=type('Meta', (object,), dict(model=model, fields=fields))
        )
    )
    return filter_class


def build_query_objs():
    queries = {}
    models = apps.get_app_config(APPLICATION_NAME).get_models()

    for model in models:
        model_name = model.__name__
        if model_name not in custom_models:
            meta_class = create_model_object_meta(model)

            node = type('{model_name}'.format(model_name=model_name),
                        (DjangoObjectType,),
                        dict(
                            Meta=meta_class,
                            _id=Int(name='_id'),
                            resolve__id=id_resolver,
            )
            )
            queries.update({model_name: PlainTextNode.Field(node)})
            queries.update({
                'all_{model_name}'.format(model_name=model_name):
                    DjangoFilterConnectionField(
                        node, filterset_class=create_model_in_filters(model))
            })
    return queries


BusinessLogicQuery = type('Query', (ObjectType,), build_query_objs())
