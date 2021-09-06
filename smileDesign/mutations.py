import graphene
import requests
from businessLogic.models import *
import json
from graphene_file_upload.scalars import Upload
from .models import *


class SmileDesignImages(graphene.InputObjectType):
    teeth_less_image = Upload(required=False)
    smile_image_result = Upload(required=False)


class UpdateSmileDesign(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        doctor_id = graphene.Int(required=True)
        patient_id = graphene.Int(required=True)
        smile_design_images = SmileDesignImages(required=False)
        smile_color = graphene.String(required=False)
        smile_category = graphene.String(required=False)
        smile_design_state = graphene.String(required=False)

    def mutate(self, info, doctor_id, patient_id, smile_design_images, smile_color, smile_category, smile_design_state):
        smile_color = SmileColor.objects.get(name=smile_color)
        smile_category = SmileCategory.objects.get(
            name=smile_category)
        smile_design = SmileDesignService.objects.get(patient__pk=patient_id, doctor__pk=doctor_id)
        smile_design.related_smile_color = smile_color
        smile_design.related_smile_category = smile_category
        smile_design.state = smile_design_state
        if smile_design_images:
            if "teeth_less_image" in smile_design_images.keys():
                smile_design.smile_image_result = smile_design_images["teeth_less_image"]
            if "smile_image_result" in smile_design_images.keys():
                smile_design.smile_image_result = smile_design_images["smile_image_result"]
            smile_design.save()
        else:
            smile_design.save()
        return UpdateSmileDesign(status="Success")


class SmileDesignMutations(graphene.ObjectType):
    update_smile_design = UpdateSmileDesign.Field()
