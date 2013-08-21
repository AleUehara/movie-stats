from django.db import models

# Create your models here.
class IMDBAccount(models.Model):
    you_IMDB_ID = models.CharField(max_length=20)