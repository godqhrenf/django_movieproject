from django.db import models

class MovieRating(models.Model):
    userId = models.PositiveIntegerField()
    movieId = models.PositiveIntegerField()
    rating = models.FloatField()