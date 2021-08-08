from django_filters.filters import Filter
import graphene

from businessLogic.schema import BusinessLogicQuery, BusinessLogicQueryCustom
from extendProfile.mutations import BaseMutation
from businessLogic.mutations import BusinessLogicMutations
from notification.mutations import NotificationMutations
from smileDesign.mutations import SmileDesignMutations
from extendProfile.schema import extendProfileQuery
from smileDesign.schema import smileDesignQuery
from notification.schema import notificationQuery
# from businessLogic.mutations import FilterPatient, FilterOrderByPatient, FilterLabByName

from smileDesign.models import SmileDesignService
# from graphene_subscriptions.events import CREATED, UPDATED



class Query(BusinessLogicQuery, BusinessLogicQueryCustom, smileDesignQuery, extendProfileQuery, notificationQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass




class Mutations(BaseMutation, BusinessLogicMutations, NotificationMutations, SmileDesignMutations, graphene.ObjectType):
    pass



# class Subscription(graphene.ObjectType):
#     ai_status = graphene.String()

#     def resolve_ai_status(self, info):
#         return self.filter(
#             lambda event:
#                 event.operation == UPDATED and
#                 isinstance(event.instance, SmileDesignService) and
#                 event.instance.status == "ready"
#         ).map(lambda event: event.instance)


schema = graphene.Schema(query=Query, mutation=Mutations)
