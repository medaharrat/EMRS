from django.db import models

# Create your models here.
class Movie(models.Model):  
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)  
    description = models.CharField(max_length=500) 
    rating = models.FloatField() 
    image = models.CharField(max_length=200)
    url = models.CharField(max_length=150)
    release_date = models.CharField(max_length=100)
    class Meta:  
        db_table = "Movies"  
    #Constructor
    def __init__(self, id, title, description, rating, image, url, release_date):
        self.id = id
        self.title = title
        self.description = description
        self.rating = rating
        self.image = image
        self.url = url
        self.release_date = release_date
    #Getters
    def getId(self): return self.id
    def getTitle(self): return self.title
    def getDescription(self): return self.description
    def getRating(self): return self.rating
    def getImage(self): return self.image
    def getURL(self): return self.url
    def geReleaseDate(self): return self.release_date
