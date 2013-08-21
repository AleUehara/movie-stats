from django.db import models

# Create your models here.
class IMDBAccount(models.Model):
    your_IMDB_ID = models.CharField(max_length=20)