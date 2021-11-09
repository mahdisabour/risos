from businessLogic.models import Lab, Doctor
import graphene
import graphene_django
from extendProfile.models import Location, Profile
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
import django_filters
from django.db.models import ImageField, CharField
from graphene import relay, ObjectType, Schema, Field, Int
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance


custom_model = ["Tutorial", "Location"]

# Set this to your Django application name
APPLICATION_NAME = 'extendProfile'


class PlainTextNode(relay.Node):
    class Meta:
        name = 'extendProfileNode'

    @staticmethod
    def to_global_id(type, id):
        return '{}:{}'.format(type, id)

    @staticmethod
    def from_global_id(global_id):
        return global_id.split(':')


def id_resolver(self, *_):
    return self.id


# exempted_field_types = (ArrayField, GenericForeignKey, JSONField)
exempted_field_types = (GenericForeignKey, ImageField)
exempted_field_names = ('_field_status', 'location')


class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass


def generate_filter_fields(model):
    # May want to add special string methods here eg istartswith
    return {f.name: ['exact', 'in'] for f in model._meta.get_fields()
            if not isinstance(f, exempted_field_types) and f.name not in exempted_field_names}


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
        if model_name not in custom_model:
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


class LabNode(DjangoObjectType):
    class Meta:
        model = Lab

class DoctorNode(DjangoObjectType):
    class Meta:
        model = Doctor


class GetNearest(graphene.ObjectType):
    get_nearest_lab = graphene.List(
        LabNode, profile_id=graphene.Int(), first=graphene.Int())

    get_nearest_doctor = graphene.List(
        DoctorNode, profile_id=graphene.Int(), first=graphene.Int())

    def resolve_get_nearest_lab(self, info, **kwargs):
        user_location = Location.objects.get(
            related_profile__id=kwargs["profile_id"]).point
        nearest = Location.objects.annotate(distance=Distance(
            "point", user_location)).order_by('distance')
        output = [Lab.objects.get(related_profile=loc.related_profile) for loc in nearest if loc.related_profile.role == "lab"][:kwargs["first"]]
        return output


    def resolve_get_nearest_doctor(self, info, **kwargs):
        user_location = Location.objects.get(
            related_profile__id=kwargs["profile_id"]).point
        nearest = Location.objects.annotate(distance=Distance(
            "point", user_location)).order_by('distance')
        output = [Doctor.objects.get(related_profile=loc.related_profile) for loc in nearest if loc.related_profile.role == "doctor"][:kwargs["first"]]
        return output


extendProfileQuery = type('Query', (ObjectType,), build_query_objs())
