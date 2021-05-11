import graphene

from businessLogic.schema import BusinessLogicQuery
from extendProfile.mutations import  BaseMutation
from extendProfile.schema import extendProfileQuery
from smileDesign.schema import smileDesignQuery


class Query(BusinessLogicQuery, smileDesignQuery, extendProfileQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=BaseMutation)
