from django.db import models
import datetime


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5, unique=True)
    data_last_updated = models.DateTimeField(auto_now_add=True)
    latest_tweets_pos = models.PositiveIntegerField(default=0)
    latest_tweets_neg = models.PositiveIntegerField(default=0)
    top_tweets_pos = models.PositiveIntegerField(default=0)
    top_tweets_neg = models.PositiveIntegerField(default=0)
