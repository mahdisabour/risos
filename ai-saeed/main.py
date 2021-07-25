from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from aiHandler import *



class Image(BaseModel):
    url: str


app = FastAPI()


@app.post("/")
def root(image:Image):
    print(f"request is now here in root function")

    resp = get_image_from_url(image.url)
    
    if not resp["error"]:
        try:
            img = removeTeeth(resp["image"])
            img_base_64 = cv2Base64(img)
            # img_base_64 = "data:image/png;base64, " +  str(img_base_64)
            return {"status_code":"200" , "image":img_base_64, "shape":None}
        except:
            return {"status_code":"400", "image":None, "shape":None}
    else:
        return {"status_code":"400", "image":None, "shape":"circule"} 