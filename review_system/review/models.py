from django.db import models

# Create your models here.
class Review_Product(models.Model):
    text = models.TextField()
    rating = models.FloatField(default='')