from django.db import models

# Create your models here.
class Movies(models.Model):  
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)  
    url = models.CharField(max_length=150)
    class Meta:  
        db_table = "seen_movies"  

