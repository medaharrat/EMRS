from django.shortcuts import render
#Imports for the model
from keras.models     import load_model
from time             import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing       import image
import cv2
import numpy as np

# imports for WebScraping
from bs4 import BeautifulSoup
import urllib.request


# Create your views here.
def Home(request):  
    return render(request,'index.html')  

def Capture(request):
    return render(request,'capture.html') 

def GetMovies(request, mood):
    category = GetMatchGenre(mood)
    movies = {}
    filmCounter = 0

    # get the html page of every category
    html_page = urllib.request.urlopen("https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&num_votes=5000,&genres={}&sort=user_rating,desc&start=1&ref_=adv_nxt".format(category))
    soup = BeautifulSoup(html_page, "lxml")

    # filling the movies into movie list
    for img in zip(soup.findAll("img", class_="loadlate"),soup.findAll("div", class_="lister-item-content"), soup.findAll("span", class_="lister-item-year text-muted unbold"), soup.findAll("div", class_="inline-block ratings-imdb-rating")):

        movies[filmCounter] = {"name" : img[0]['alt'],"released_date" : img[2].text, "rating" : img[3].find("strong").text,"image_url" :img[0]['loadlate'], "description" : img[1].findChildren('p')[1].text, }

        filmCounter += 1
        
        

   # OUR SCRAPER GOES HERE

    return render(request,'movies.html', {'mood':mood, 'movies':movies})

def GetMatchGenre(emotion):
    if(emotion == "Sad"): 
        genre = 'Drama'
    elif(emotion == "Happy"): 
        genre = 'Musical'
    elif(emotion == "Angry"): 
        genre = 'Comedy'
    elif(emotion == "Surprise"): 
        genre = 'Fantasy'
    elif(emotion == "Neutral"): 
        genre = 'Western'
    return genre

def Seen(request):
    return render(request,'seen.html')  

def HandlePicRequest(request):
    face_classifier = cv2.CascadeClassifier("./EMRS/haarcascade_frontalface_default.xml")
    classifier = load_model("./EMRS/Emotion_little_vgg.h5")
    class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

    labels = []

    img = cv2.imread("./EMRS/static/img/happy.jpg")
    
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




