from fastapi import FastAPI 
from pydantic import BaseModel

from pyteeth import Teeth

class Image(BaseModel):
    url: str


app = FastAPI()



@app.post("/")
def root(image:Image):
    print(image.url)
    teeth = Teeth(image.url)
    teeth.detect_top_six_teeth_for_edit(teeth.resized_image)
    #return image
    return {"message":"200"} #teeth.coords}