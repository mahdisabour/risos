# https://github.com/timothyjlaurent/auto-graphene-django/blob/master/auto-graphene-django/graphql.py
from django.apps import apps
# from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
import django_filters
from django.db.models import ImageField
# from django.contrib.gis.db.models.fields import PointField
from graphene import relay, ObjectType, Schema, Field, Int
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField



custom_model = []


# # Set this to your Django application name
APPLICATION_NAME = 'smileDesign'


class PlainTextNode(relay.Node):
    class Meta:
        name = 'smileDesignNode'

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
exempted_field_names = ('_field_status',)


class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass


def generate_filter_fields(model):
    # May want to add special string methods here eg istartswith
    return {f.name: ['in'] for f in model._meta.get_fields()
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

    custome_filter = {}
    if model_name == "Teeth":
        custome_filter = {'filter_by_color': django_filters.CharFilter(
            field_name='related_smile_color__name', lookup_expr='iexact'),
            'filter_by_category' : django_filters.CharFilter(
            field_name='related_smile_category__name', lookup_expr='iexact')
        }

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
                    DjangoFilterConnectionField(node, filterset_class=create_model_in_filters(model))
            })
    # queries['debug'] = Field(DjangoDebug, name='__debug')
    return queries


smileDesignQuery = type('Query', (ObjectType,), build_query_objs())
