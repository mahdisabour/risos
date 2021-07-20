#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
=====================
Classifier comparison
=====================

Originally a comparison of a several classifiers in scikit-learn on synthetic datasets.
Turned into a face shape classifier comparison.
"""
# Original Code source: Gaël Varoquaux
#              Andreas Müller
# Modified for documentation by Jaques Grobler
# Modified for HADETH by Saeed Jamshidiha
# License: BSD 3 clause


import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import VotingClassifier
import pandas as pd
import dlib
import os
import cv2
from scipy.interpolate import CubicSpline
import math
from joblib import dump, load
import time
import requests

t0 = time.time()
# Load dataset

def classifyAndRemoveTeeth(image):

    data = pd.read_csv('Data.csv')
    original_labels = data['label']
    y = []

    # Turn qualitative labels to quantitative labels
    LABELs = ['square', 'round', 'oval', 'heart', 'oblong']
    for item in original_labels:
        y.append(LABELs.index(item))
    Y = np.array(y)

    # Sorry for the dirty fix!
    del data['label']
    x = np.array(data)

    # preprocess dataset, split into training and test sets
    scaler = StandardScaler()
    X = scaler.fit_transform(x)

    def dist(x1,y1,x2,y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    #Load face detector
    detector = dlib.get_frontal_face_detector()
    #Load face key detection model
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    # current_dir = os.listdir(os.getcwd())
    # img_files = [item for item in current_dir if (item.endswith('.jpg') or item.endswith('.JPG'))]
    # img_path = "images.jpeg"
    # img = cv2.imread(img_path)
    img = image
    dets = detector(img, 1)
    height = np.size(img,0)
    width = np.size(img,1)
    x_mouth = []
    y_mouth = []
    del x, y
    x = []
    y = []
    l = []

    for k, d in enumerate(dets):
        # Detect face key points in box d
        shape = predictor (img, d)
        for j in range(68):
            x.append(shape.part(j).x)
            y.append(shape.part(j).y)
        for i in range(20):
            x_mouth.append(shape.part(i+48).x)
            y_mouth.append(shape.part(i+48).y)

    try:
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

        #Interpolation
        cs4 = CubicSpline(x[8:15], y[8:15])
        cs4_int = CubicSpline.integrate(cs4,x[8],x[16])
        cs3 = CubicSpline(y[0:8], x[0:8])
        cs3_int = CubicSpline.integrate(cs3,y[0],y[8])


        #removing Teeth
        for i in range (height) :
            for j in range (width) :
                if cs2 (j) >= i >= cs1 (j) :
                    img [i, j, :] = (0, 0, 0)
    except Exception as e:
        print(e)
        quit()

    ax1 = dist(x[0],y[0], x[16],y[16])
    ax2 = dist((x[0]+x[16])//2,(y[0]+y[16])//2, x[8],y[8])
    Test = []
    Test.append(ax1/ax2)
    Test.append(dist(x[62],y[62],x[66],y[66]))
    Test.append(np.arctan2(y[8] - y[0], x[8] - x[0]))
    Test.append(np.arctan2(y[16] - y[8], x[16] - x[8]))
    Test.append(np.arctan2(y[8] - y[4], x[8] - x[4]) - np.arctan2(y[8] - y[12], x[8] - x[12]))
    Test.append(np.arctan2(y[16] - y[0], x[16] - x[0]))
    Test.append(2*cs3_int/(ax1*ax2))
    Test.append(2*(np.pi*ax1*ax2/8-(ax1*ax2/4))/(ax1*ax2))
    Test.append(cs4_int/(ax1*ax2))
    Test = np.array(Test)
    Test = Test.reshape((1, -1))
    Test = scaler.transform(Test)

    # iterate over classifiers
    try:
        eclf = load('eclf.joblib')
    except:
        #est = []
        #for i in range(len(names)):
        #    est.append((names[i], classifiers[i]))
        #eclf = VotingClassifier(estimators=est)
        eclf = MLPClassifier(alpha=1, max_iter=1000)
        eclf.fit(X, Y)
        dump(eclf, 'eclf.joblib')
    print('MLP', LABELs[int(eclf.predict(Test))])
    duration = time.time()-t0 
    print(duration)
    data = {"image":img, "shape": LABELs[int(eclf.predict(Test))], "duration":duration}
    return data



def get_image_from_url(self , url):
    
    resp = requests.get(url, stream=True).raw
    if resp.status != 200:
        return {
            "error" : f"image get url return with code: {resp.status}", 
            "image": None}
    
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return {"image": image, "error": None}

    # return {"succes" : f"image obtained"}



if __name__ == "__main__":
    print("__ai-aida__")
    