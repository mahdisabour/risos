from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from pyteeth import Teeth

class Image(BaseModel):
    url: str


app = FastAPI()





@app.post("/")
def root(image:Image):
    print(f"request is now here in root function")
    teeth = Teeth()

    resp = teeth.get_image_from_url(image.url)
    if "error" in resp:
        raise HTTPException(status_code=400, detail=resp["error"])
    
    coords = teeth.detect_top_six_teeth_for_edit(teeth.image)
    if coords is None:
        raise HTTPException(status_code=400, detail="image doesnt contain teeth to detect")
    
    return {"status_code":"200" , "coords":coords} 