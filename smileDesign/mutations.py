import graphene
from .models import SmilePlot, OutRectangle, TeethCoordinate, SmileDesignService
import requests 
from businessLogic.models import *
from .tasks import aiConnection
import json

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



class CreateSmileDesign(graphene.Mutation):
    status = graphene.String()
    detail = graphene.String()
    smile_design_id = graphene.ID()

    class Arguments:
        # service_id = graphene.ID(required=True)
        patient_id = graphene.ID(required=True)
    
    def mutate(self, info, patient_id):
        patient = Patient.objects.get(id=patient_id)
        patient_pic = patient.patient_pic
        smile_image = patient_pic.smile_image
        image_url = smile_image.url
        ai_response = aiConnection(image_url=image_url)
        data = json.loads(ai_response.text)
        if data["status_code"] == "200":
            smile_design = SmileDesignService()
            smile_design.save()
            rect_angle = smile_design.smile_plot.first().out_rectangle.first().rect_angle
            coords = data["coords"]
            for key, val in coords.items():
                if val:
                    setattr(rect_angle, key, val)
            rect_angle.save()
            return CreateSmileDesign(status="Sucsess", detail="done", smile_design_id=smile_design.id)
        else:
            return CreateSmileDesign(status="Failed", detail=data["detail"])



class SmileDesignMutations(graphene.ObjectType):
    coordinates_mutation = CoordinatesMutations.Field()
    create_smile_design = CreateSmileDesign.Field()
