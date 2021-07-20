from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from .classify import *



class Image(BaseModel):
    url: str


app = FastAPI()


@app.post("/")
def root(image:Image):
    print(f"request is now here in root function")

    resp = get_image_from_url(image.url)
    
    if resp["image"]:
        data = classifyAndRemoveTeeth(resp["image"])
        return {"status_code":"200" , "image":data["image"], "duration": data["duration"]}
    else:
        return {"status_code":"400", "image":None} 