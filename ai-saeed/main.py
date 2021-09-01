from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from aiHandler import *



class Image(BaseModel):
    url: str
    smile_design_id: int


app = FastAPI()


@app.post("/")
def root(image:Image):
    print(f"request is now here in root function")

    resp = get_image_from_url(image.url)
    smile_design_id = image.smile_design_id
    
    if not resp["error"]:
        try:
            img = removeTeeth(resp["image"], smile_design_id)
            img_base_64 = cv2Base64(img)
            # img_base_64 = "data:image/png;base64, " +  str(img_base_64)
            print(smile_design_id, "-> 200")
            return {"status_code":"200" , "image":img_base_64, "shape":None}
        except:
            print(smile_design_id, "-> 400")
            return {"status_code":"400", "image":None, "shape":None}
    else:
        print(smile_design_id, "-> 400")
        return {"status_code":"400", "image":None, "shape":"circule"} 