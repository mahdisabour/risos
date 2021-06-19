import graphene
from .models import SmilePlot, OutRectangle, TeethCoordinate, SmileDesignService


class RectAngleInput(graphene.InputObjectType):
    x1 = graphene.Int(required=False)
    y1 = graphene.Int(required=False)
    x2 = graphene.Int(required=False)
    y2 = graphene.Int(required=False)


class CoordinatesMutations(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        related_smile_design_id = graphene.Int(required=True)
        outer_rectangle = RectAngleInput(required=False)
        tooth_coordinates = graphene.List(RectAngleInput, required=False)

    def mutate(self, info, **kwargs):
        smile_design = SmileDesignService.objects.get(
            id=kwargs["related_smile_design_id"])
        smile_plot = SmilePlot.objects.filter(
            related_smile_design=smile_design).first()

        # outer rectangle for smile plot
        # bug(one to one filed bug (you should fix it))
        out_rectangle = OutRectangle.objects.filter(
            related_smile_plot=smile_plot).first()
        for key, val in kwargs["outer_rectangle"].items():
            if val:
                setattr(out_rectangle.rect_angle, key, val)
        out_rectangle.rect_angle.save()


        # tooth coordinates mutations
        for teeth in smile_plot.teeth_coordinates.all():
            rect_angel = teeth.rect_angle
            if teeth.sequence >= len(kwargs["tooth_coordinates"]):
                break
            for key, val in kwargs["tooth_coordinates"][teeth.sequence].items():
                if val:
                    setattr(rect_angel, key, val)
            rect_angel.save()

        return CoordinatesMutations(status="Success")



class SmileDesignMutations(graphene.ObjectType):
    coordinates_mutation = CoordinatesMutations.Field()