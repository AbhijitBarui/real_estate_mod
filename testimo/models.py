from django.db import models
from datetime import datetime

class Testimo(models.Model):
    name = models.CharField(max_length=100)
    listing_title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    review = models.TextField(blank=True)
    review_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.listing_title