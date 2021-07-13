# from fastapi import FastAPI , HTTPException
# from pydantic import BaseModel

# from pyteeth import Teeth

# class Image(BaseModel):
#     url: str


# app = FastAPI()


# @app.post("/")
# def root(image:Image):
#     print(f"request is now here in root function")
#     teeth = Teeth()

#     resp = teeth.get_image_from_url(image.url)
#     if "error" in resp:
#         detail = resp["error"]
#         return {"status_code":"400" , "detail":f"{detail}"} 
#         # raise HTTPException(status_code=400, detail=resp["error"])
    
#     coords = teeth.detect_top_six_teeth_for_edit(teeth.image)
#     if coords is None:
#         return {"status_code":"400" , "detail":"image does'nt contain teeth to detect"} 
#         # raise HTTPException(status_code=400, detail="image doesnt contain teeth to detect")
#     coords = {"x1":coords[0], "y1":coords[1], "x2":coords[2], "y2":coords[3]}
#     return {"status_code":"200" , "coords":coords} 