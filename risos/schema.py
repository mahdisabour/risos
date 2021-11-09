import graphene
from businessLogic.schema import BusinessLogicQuery, CustomeBusinessLogic
from extendProfile.mutations import BaseMutation
from businessLogic.mutations import BusinessLogicMutations
from notification.mutations import NotificationMutations
from smileDesign.mutations import SmileDesignMutations
from extendProfile.schema import extendProfileQuery, GetNearest
from smileDesign.schema import smileDesignQuery
from notification.schema import notificationQuery
from businessLogic.schema import GetReportByLabId


class Query(BusinessLogicQuery, smileDesignQuery, extendProfileQuery, notificationQuery, GetReportByLabId, GetNearest, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutations(BaseMutation, BusinessLogicMutations, NotificationMutations, SmileDesignMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutations)
