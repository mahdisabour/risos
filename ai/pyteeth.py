from urllib.request import urlopen

import cv2 
import numpy as np

from detector import ObjectDetector

class Teeth():
    def __init__(self , url):
        print("__init__")
        self.coords = 0
        self.top_six_image = 0
        
        req = urlopen(url)
        print(req)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image =  cv2.imdecode(arr, -1)
        print("reeeeeeeeeeeeeeeeeeeeeeeeeeeeq")
        
        print("__init__")
        self.resized_image = None
        self.reshape_image(image)
        self.image = image

    def reshape_image(self , image=None):
        # if image == None:
        #     image = self.image
        # if image.shape[0] < 1000 and image.shape[1] < 1000:
        #     return image
        # if image.shape[0] > image.shape[1]:
        #     ratio = 640 / image.shape[0] 
        # else : 
        #     ratio = 640/ image.shape[1]
        # resized_image = cv2.resize(image, (0,0), fx=ratio, fy=ratio) 
        ratiox = 800/image.shape[1]
        ratioy = 600/image.shape[0]
        resized_image = cv2.resize(image, (0,0), fx=ratiox, fy=ratioy) 
        
        
        self.resized_image = resized_image
        # self.detect_top_six_teeth_for_edit(resized_image)
        return resized_image
    
    def detect_top_six_teeth_for_edit(self , image):
        image = self.reshape_image(image)

        detector = ObjectDetector(loadPath="teeth_detector.svm")
        x,y,xb,yb = detector.detect(image)
        print(x,y,xb,yb)
        cv2.rectangle(image,(x,y),(xb,yb),(0,0,255),2)
        cv2.putText(image,"top6_teeth",(x+5,y-5),cv2.FONT_HERSHEY_SIMPLEX,1.0,(128,255,0),2)
        print("::")
        self.coords = (x,y,xb,yb)
        self.top_six_image = image
        #return (x,y,xb,yb)
        #return image

    def detect_each_tooth_for_edit(self , image , coords):
        x , y , xb , yb = coords
        w = xb-x
        h = yb-y
        w_step = w // 6
        print(w_step , x,y,xb,yb ,w)
        for x_line in range(x  , xb , w_step):
            cv2.line(image, (x_line, y), (x_line, yb), (0, 255, 0), thickness=2)
        
        return image

if __name__ == "__main__":
    image = cv2.imread("IMG_6031.JPG")
    teeth = Teeth(image=image)
    print(teeth.top_six_image)
