from django.db import models
import datetime


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    data_last_updated = models.DateTimeField(auto_now_add=True)
    average_sentiment = models.DecimalField(default=0, max_digits=3, decimal_places=2)
