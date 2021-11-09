import dlib
import cv2
from scipy.interpolate import interp1d
import numpy as np
from scipy.interpolate import CubicSpline
from scipy import signal
import requests
import base64



def get_image_from_url(url):
    resp = requests.get(url, stream=True).raw
    if resp.status != 200:
        return {
            "error" : f"image get url return with code: {resp.status}", 
            "image": None, 
            "status": resp.status}
    
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return {"image": image, "error": None, "status": resp.status}



# def removeTeeth(img, smile_design_id):
#     # Load face detector
#     # Load face detector
#     detector = dlib.get_frontal_face_detector()

#     # Load face key detection model
#     predictor_path = "./shape_predictor_68_face_landmarks.dat"
#     predictor = dlib.shape_predictor(predictor_path)

#     # Load image and convert to HSV
#     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # Detect landmarks
#     dets = detector(img, 1)
#     height = np.size(img,0)
#     width = np.size(img,1)
#     xm = []
#     ym = []
#     for k, d in enumerate(dets):
#         # Detect face key points in box d
#         shape = predictor (img, d)
#         for i in range(20):
#             xm.append(shape.part(i+48).x)
#             ym.append(shape.part(i+48).y)

    

#     # The landmarks of the lips
#     x_o = [xm[0],xm[11],xm[10],xm[9],xm[8],xm[7],xm[6]]
#     y_o = [ym[0],ym[11],ym[10],ym[9],ym[8],ym[7],ym[6]]

#     # The landmarks of the mouth
#     xm1 = xm[12:17]
#     ym1 = ym[12:17]
#     xm2 = [xm[12],xm[-1], xm[-2],xm[-3],xm[16]]
#     ym2 = [ym[12],ym[-1], ym[-2],ym[-3],ym[16]]

#     # Interpolate lips/mouth
#     olow = interp1d(xm[0:7], ym[0:7])
#     ohigh = interp1d(x_o, y_o)
#     inlow = CubicSpline(xm1, ym1)
#     inhigh = CubicSpline(xm2, ym2)

#     # Obtain saturation histogram
#     s = []
#     for z in range(min(xm[0:7]), max(xm[0:7]), 1):
#         low, high = int(inlow(z)), int(inhigh(z))
#         for w in range(low, high, 1):
#             s.append(hsv_img[w,z,1])
#     hist,bins = np.histogram(s,256,[0,256])

#     # Smooth the histogram by performing a rolling average
#     w = 10 # Rolling average window size
#     hist = np.convolve(hist, np.ones(w), 'valid') / w

#     # Detect the local minima of the histogram
#     minimums = signal.argrelextrema(hist, np.less)
#     minis = minimums[0]
#     thres = minis[int(minis.shape[0]/2)]

#     # Generate the output image
#     nimg = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
#     for z in range(min(xm[0:7]), max(xm[0:7]), 1):
#         low, high = int(inlow(z)), int(inhigh(z))
#         for w in range(low, high, 1):
#             if hsv_img[w,z,1] < thres:
#                 nimg[w, z, 3] = 0
    
#     return nimg



def resizeImage(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(image, dim, interpolation = inter)
    return resized




def removeTeeth(img, smile_design_id, detector, predictor):
    img = resizeImage(img, width=250)
    dets = detector(img, 1)
    height = np.size(img, 0)
    width = np.size(img, 1)
    x_mouth = []
    y_mouth = []
    # del x, y
    x = []
    y = []
    l = []
    c_img = np.zeros((height,width, 4))
    for k, d in enumerate(dets):
        # Detect face key points in box d
        shape = predictor(img, d)
        for j in range(68):
            x.append(shape.part(j).x)
            y.append(shape.part(j).y)
        for i in range(20):
            x_mouth.append(shape.part(i+48).x)
            y_mouth.append(shape.part(i+48).y)


    for i in range(17):
        l.append((x[i],y[i]))
    #Key points for mouth's inner edge
    xm1 = x_mouth[12:17]
    ym1 = y_mouth[12:17]
    xm2 = [x_mouth[12],x_mouth[-1], x_mouth[-2],x_mouth[-3],x_mouth[16]]
    ym2 = [y_mouth[12],y_mouth[-1], y_mouth[-2],y_mouth[-3],y_mouth[16]]

    #Interpolation
    cs1 = CubicSpline (xm1, ym1)
    cs2 = CubicSpline (xm2, ym2)

    cs4 = CubicSpline(x[8:15], y[8:15])
    cs4_int = CubicSpline.integrate(cs4,x[8],x[16])
    cs3 = CubicSpline(y[0:8], x[0:8])
    cs3_int = CubicSpline.integrate(cs3,y[0],y[8])
    c_img = cv2.cvtColor (img, cv2.COLOR_BGR2BGRA)
    # removing Teeth
    for i in range (height) :
        for j in range (width) :
            if cs2 (j) >= i >= cs1 (j) :
                c_img [i, j, :] = (0, 0, 0, 0)

    return c_img
    





def cv2Base64(img):
    retval, buffer = cv2.imencode(".png", img)
    img_as_code = base64.b64encode(buffer)
    return img_as_code





if __name__ == "__main__":
    print("__ai-saeed__")
    