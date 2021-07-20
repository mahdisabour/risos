import dlib
import cv2
from scipy.interpolate import interp1d
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline
from scipy import signal

# Load face detector
detector = dlib.get_frontal_face_detector()

# Load face key detection model
predictor_path = "./shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

# Load image and convert to HSV
imgfile = 'test.jpeg'
img = cv2.imread (imgfile)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Detect landmarks
dets = detector(img, 1)
height = np.size(img,0)
width = np.size(img,1)
xm = []
ym = []
for k, d in enumerate(dets):
    # Detect face key points in box d
    shape = predictor (img, d)
    for i in range(20):
        xm.append(shape.part(i+48).x)
        ym.append(shape.part(i+48).y)

# The landmarks of the lips
x_o = [xm[0],xm[11],xm[10],xm[9],xm[8],xm[7],xm[6]]
y_o = [ym[0],ym[11],ym[10],ym[9],ym[8],ym[7],ym[6]]

# The landmarks of the mouth
xm1 = xm[12:17]
ym1 = ym[12:17]
xm2 = [xm[12],xm[-1], xm[-2],xm[-3],xm[16]]
ym2 = [ym[12],ym[-1], ym[-2],ym[-3],ym[16]]

# Interpolate lips/mouth
olow = interp1d(xm[0:7], ym[0:7])
ohigh = interp1d(x_o, y_o)
inlow = CubicSpline(xm1, ym1)
inhigh = CubicSpline(xm2, ym2)

# Obtain saturation histogram
s = []
for z in range(min(xm[0:7]), max(xm[0:7]), 1):
    low, high = int(inlow(z)), int(inhigh(z))
    for w in range(low, high, 1):
        s.append(hsv_img[w,z,1])
hist,bins = np.histogram(s,256,[0,256])

# Smooth the histogram by performing a rolling average
w = 10 # Rolling average window size
hist = np.convolve(hist, np.ones(w), 'valid') / w

# Detect the local minima of the histogram
minimums = signal.argrelextrema(hist, np.less)
minis = minimums[0]
thres = minis[int(minis.shape[0]/2)]

# Generate the output image
nimg = img.copy()
for z in range(min(xm[0:7]), max(xm[0:7]), 1):
    low, high = int(inlow(z)), int(inhigh(z))
    for w in range(low, high, 1):
        if hsv_img[w,z,1] < thres:
            nimg[w, z, :] = 0
cv2.imwrite('output.jpg', nimg)
