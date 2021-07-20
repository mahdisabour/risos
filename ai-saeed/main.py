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
        img = removeTeeth(resp["image"])
        img_base_64 = cv2Base64(img)
        return {"status_code":"200" , "image":img_base_64}
    else:
        return {"status_code":"400", "image":None} 