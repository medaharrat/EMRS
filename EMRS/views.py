from django.shortcuts import render
#Imports for the model
from keras.models     import load_model
from time             import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing       import image
import cv2
import numpy as np
#Imports for webscaping
from bs4 import BeautifulSoup as SOUP 
import re 
import requests as HTTP 

# Create your views here.
def Home(request):  
    return render(request,'index.html')  

def Capture(request):
    return render(request,'capture.html') 

def GetMovies(request, mood):
    movies = ["movviiiie"]
   
   # OUR SCRAPER GOES HERE

    return render(request,'movies.html', {'mood':mood, 'movies':movies})

def GetMatchGenre(emotion):
    if(emotion == "Sad"): 
        genre = 'drama'
    elif(emotion == "Happy"): 
        genre = 'musical'
    elif(emotion == "Angry"): 
        genre = 'family'
    elif(emotion == "Surprise"): 
        genre = 'film_noir'
    elif(emotion == "Neutral"): 
        genre = 'western'
    return genre

def Seen(request):
    return render(request,'seen.html')  

def HandlePicRequest(request):
    face_classifier = cv2.CascadeClassifier("C:/Users/aharr/OneDrive/Bureau/emotion_detection-master/E-MRS/app/EMRS/haarcascade_frontalface_default.xml")
    classifier = load_model("C:/Users/aharr/OneDrive/Bureau/emotion_detection-master/E-MRS/app/EMRS/Emotion_little_vgg.h5")
    class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

    labels = []

    img = cv2.imread("C:/Users/aharr/OneDrive/Bureau/emotion_detection-master/E-MRS/app/EMRS/static/img/angry.jpg")
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)
            preds = classifier.predict(roi)[0]
            label=class_labels[preds.argmax()]
            label_position = (x,y)

    return render(request,'confirm.html', {'mood':label})




