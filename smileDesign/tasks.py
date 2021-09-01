from risos.celery import app
import requests
import base64
from .models import FaceShape, SmileDesignService
import os
from django.core.files.images import get_image_dimensions

@app.task
def aiConnection(image_url, smile_design_id, ai_url="http://ai:4557"):
    print(f"http://risos:8000{image_url}")
    data = {
        "url": f"http://risos:8000{image_url}",
        "smile_design_id": smile_design_id,
    }
    response = requests.post(ai_url,json=data)
    return response.json()


@app.task
def aiReady(ai_response, smile_design_id, patient_id):
    smile_design = SmileDesignService.objects.get(id=smile_design_id)
    if ai_response["status_code"] == "200":
        img_data = ai_response["image"]
        data = base64.b64decode(img_data)
        new_path = f"{smile_design_id}_{patient_id}.png"
        image_path = f"./mediafiles/{new_path}"
        with open(image_path, "wb") as f:
            f.write(data)
        shape = ai_response["shape"]
        shape_object = FaceShape.objects.filter(name=shape)
        if shape_object.exists():
            smile_design.shape = shape_object.first
        smile_design.teeth_less_image = new_path
        smile_design.status = "ready"
        print("Kiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiir")
        width, heigth = get_image_dimensions(smile_design.teeth_less_image.file)
        smile_design.width = width
        smile_design.heigth = heigth
        smile_design.save()
    else:
        smile_design.status = 'improper image'
        smile_design.save()
    
    
