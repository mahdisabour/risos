import django
from django.apps import apps
from django.contrib.contenttypes.fields import GenericForeignKey
import django_filters
from django.db.models import ImageField, CharField
from django_filters.filters import CharFilter, NumberFilter
from graphene import relay, ObjectType, Schema, Field, Int
from graphene.relay.connection import Connection
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


class ExtendedConnection(Connection):
    class Meta:
        abstract = True

    total_count = Int()
    edge_count = Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length
    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class PlainTextNode(relay.Node):
    class Meta:
        name = 'businessLogicNode'

    @staticmethod
    def to_global_id(type, id):
        return id

    @staticmethod
    def from_global_id(global_id):
        return global_id.split(':')


# custom_models = ["Lab", "Doctor"]
custom_models = []

class LabNode(DjangoObjectType):
    class Meta:
        model = Lab
        # Allow for some more advanced filtering here
        filter_fields = {
            'related_profile__first_name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (PlainTextNode, )


class CustomeBusinessLogic(graphene.ObjectType):
    lab = relay.Node.Field(LabNode)
    all_lab = DjangoFilterConnectionField(LabNode)
    



APPLICATION_NAME = 'businessLogic'

class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass


def create_model_object_meta(model):
    return type('Meta',
                (object,),
                dict(model=model,
                     interfaces=(PlainTextNode,),
                     connection_class = ExtendedConnection,
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
    if model_name == "Patient":
        custome_filter = {'search_by_name': django_filters.CharFilter(
            field_name='related_profile__first_name', lookup_expr='icontains')}

    if model_name == "Lab":
        custome_filter = {
            'search_by_name': django_filters.CharFilter(
                field_name='related_profile__first_name', lookup_expr='icontains'),
            "sort_by_rate": django_filters.OrderingFilter(
                fields=('-rating','rating'),)
            }

    if model_name == "Doctor":
        custome_filter = {
            "sort_by_rate": django_filters.OrderingFilter(
                fields=('-rating','rating'),)
            }

    if model_name == "Order":
        custome_filter = {
            'search_by_name': django_filters.CharFilter(
                field_name='related_service__related_patient__related_profile__first_name', lookup_expr='icontains'
            ), 
            'doctor_id': InFilter(
                field_name='related_service__related_doctor__id', lookup_expr='in'
            ),
            'status_startwith': CharFilter(
                field_name="status", lookup_expr="istartswith"
            )
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



class ReportNode(graphene.ObjectType):
    name = graphene.String()
    number = graphene.Int()

class GetReportByLabId(graphene.ObjectType):
    get_report = graphene.List(ReportNode,lab_id=graphene.Int())

    def resolve_get_report(self, info, lab_id):
        data = Order.objects.all().values('status').annotate(total=models.Count('status', filter=models.Q(finalized_lab__id=lab_id))).order_by('total')
        output = []
        for item in data:
            output.append(ReportNode(name=item["status"], number=item["total"]))
        return output


BusinessLogicQuery = type('Query', (ObjectType,), build_query_objs())
