from django.shortcuts import render
from keras.models     import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing       import image
import cv2
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
from EMRS.models import Movie 
from django.core.paginator import Paginator

# Webcam Import 
from django.views.decorators.csrf import csrf_exempt
import base64
from PIL import Image
from django.views.decorators.csrf import ensure_csrf_cookie
from io import BytesIO
import re

# Create your views here.

def Home(request):  
    return render(request,'index.html')  

def Capture(request):
    return render(request,'capture.html') 

def GetMovies(request, mood):
    category = GetMatchGenre(mood)
    movies = []
    filmCounter = 0

    # get the html page of every category
    html_page = urllib.request.urlopen("https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=5000,&genres={}&sort=user_rating,desc&start=1&ref_=adv_nxt".format(category))
    soup = BeautifulSoup(html_page, "lxml")
    # filling the movies into movie list
    for data in zip(soup.findAll("img", class_="loadlate"),soup.findAll("div", class_="lister-item-content"), soup.findAll("span", class_="lister-item-year text-muted unbold"), soup.findAll("div", class_="inline-block ratings-imdb-rating"), soup.findAll("h3", class_="lister-item-header")):
        movie = Movie(data[4].findChildren('a')[0]['href'].split("/")[2], data[0]['alt'], data[1].findChildren('p')[1].text, float(data[3].find("strong").text), data[0]['loadlate'], "https://www.imdb.com/"+data[4].findChildren('a')[0]['href'], data[2].text)
        movies.append(movie)
        filmCounter += 1
    paginator = Paginator(movies, 6)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request,'movies.html', {'mood':mood, 'movies':movies, 'nbMovies': filmCounter, 'paginator': paginator})

def GetMatchGenre(mood):
    emotion = mood.lower()
    if(emotion == "sad"): 
        genre = 'Drama'
    elif(emotion == "happy"): 
        genre = 'Musical'
    elif(emotion == "angry"): 
        genre = 'Comedy'
    elif(emotion == "surprise"): 
        genre = 'Fantasy'
    elif(emotion == "neutral"): 
        genre = 'Western'
    return genre

@ensure_csrf_cookie
def HandlePicRequest(request):
    if request.POST:
        
        base64_data = re.sub('^data:image/.+;base64,', '', request.POST.get('image'))
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        img.save("./EMRS/static/img/face.jpg")


    face_classifier = cv2.CascadeClassifier("./EMRS/static/haarcascade_frontalface_default.xml")
    classifier = load_model("./EMRS/static/Emotion_little_vgg.h5")
    class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

    labels = []

    img = cv2.imread("./EMRS/static/img/face.jpg")
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),4)
        roi_gray = gray[y:y+h+10,x:x+w+10]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)
            preds = classifier.predict(roi)[0]
            label=class_labels[preds.argmax()]
            label_position = (x,y)

            # make a prediction on the ROI, then lookup the class

            preds = classifier.predict(roi)[0]
            label=class_labels[preds.argmax()]
            label_position = (x,y)
           
        cv2.imwrite('./EMRS/static/img/face.jpg', img) # Second image
    cv2.imshow('Emotion Detector',img)



    return render(request,'confirm.html', {'mood':label})

#def showMovie(request, movie):        
#   return render(request, "movie.html", {'movie': movie})
