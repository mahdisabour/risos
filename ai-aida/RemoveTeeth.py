import dlib
import cv2 as cv
from scipy.interpolate import CubicSpline
import numpy as np





def removeTeeth(url):
    #Load face detector
    detector = dlib.get_frontal_face_detector()
    #Load face key detection model
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    imgfile = url
    img = cv.imread (imgfile)
    dets = detector(img, 1)
    height = np.size(img,0)
    width = np.size(img,1)
    x_mouth = []
    y_mouth = []

    for k, d in enumerate(dets):
        # Detect face key points in box d
        shape = predictor (img, d)
        for i in range(20):
            x_mouth.append(shape.part(i+48).x)
            y_mouth.append(shape.part(i+48).y)
    #Key points for mouth's inner edge
    xm1 = x_mouth[12:17]
    ym1 = y_mouth[12:17]
    xm2 = [x_mouth[12],x_mouth[-1], x_mouth[-2],x_mouth[-3],x_mouth[16]]
    ym2 = [y_mouth[12],y_mouth[-1], y_mouth[-2],y_mouth[-3],y_mouth[16]]


    #Interpolation
    cs1 = CubicSpline(xm1, ym1)
    cs2 = CubicSpline(xm2, ym2)


    for i in range(height):
        for j in range(width):
            if cs2(j)>=i>=cs1(j):
                img[i,j,:] = (0,0,0)

    cv.imwrite('Teethless.jpg', img)
    return img
