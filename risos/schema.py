from django_filters.filters import Filter
import graphene

from businessLogic.schema import BusinessLogicQuery
from extendProfile.mutations import BaseMutation
from businessLogic.mutations import BusinessLogicMutations
from notification.mutations import NotificationMutations
from extendProfile.schema import extendProfileQuery
from smileDesign.schema import smileDesignQuery
from businessLogic.mutations import FilterPatient, FilterOrderByPatient


class Query(BusinessLogicQuery, smileDesignQuery, extendProfileQuery, FilterPatient, FilterOrderByPatient, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutations(BaseMutation, BusinessLogicMutations, NotificationMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
