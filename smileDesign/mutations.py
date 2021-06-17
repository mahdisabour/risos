# import graphene
# from .models import SmilePlot, OutRectangle, TeethCoordinate, SmileDesignService


# class RectAngle(graphene.InputObjectType):
#     x1 = graphene.Int(required=False)
#     y1 = graphene.Int(required=False)
#     x2 = graphene.Int(required=False)
#     y2 = graphene.Int(required=False)


# class CoordinatesMutations(graphene.Mutation):
#     status = graphene.String()

#     class Arguments:
#         related_smile_design_id = graphene.Int(required=True)
#         outer_rectangle = RectAngle(required=False)
#         tooth_coordinates = graphene.List(RectAngle)

#     def mutate(self, info, **kwargs):
#         smile_design = SmileDesignService.objects.get(
#             id=kwargs["related_smile_design_id"])
#         smile_plot = smile_design.smile_plot
#         if OutRectangle.objects.filter(related_smile_plot = smile_plot).exists:
#             out_rectangle = OutRectangle.objects.get(related_smile_plot = smile_plot)
#             out_rectangle.rect_angle = kwargs["outer_rectangle"]



        
