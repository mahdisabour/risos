import requests

import cv2 
import numpy as np

from detector import ObjectDetector

class Teeth():
    def __init__(self):
        pass
    
    def get_image_from_url(self , url):
        
        resp = requests.get(url, stream=True).raw
        if resp.status != 200:
            return {"error" : f"image get url return with code: {resp.status}"}
        
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        self.image = image 

        return {"succes" : f"image obtained"}

    def resize_image(self , image):

        ratiox = 800/image.shape[1]
        ratioy = 600/image.shape[0]
        resized_image = cv2.resize(image, (0,0), fx=ratiox, fy=ratioy)
        
        self.resized_image = resized_image

        return resized_image
    
    def detect_top_six_teeth_for_edit(self , image):
        
        image = self.resize_image(image)

        detector = ObjectDetector(loadPath="teeth_detector.svm")
        coords = detector.detect(image)
        if coords is None:
            return coords
        
        #x,y,xb,yb = coords
        #cv2.rectangle(image,(x,y),(xb,yb),(0,0,255),2)
        #cv2.putText(image,"top6_teeth",(x+5,y-5),cv2.FONT_HERSHEY_SIMPLEX,1.0,(128,255,0),2)
        #self.top_6_teeth_image = image
        
        return coords
        

    def detect_each_tooth_for_edit(self , image , coords):
        x , y , xb , yb = coords
        w = xb-x
        h = yb-y
        w_step = w // 6
        print(w_step , x,y,xb,yb ,w)
        for x_line in range(x  , xb , w_step):
            cv2.line(image, (x_line, y), (x_line, yb), (0, 255, 0), thickness=2)
        
        return image

