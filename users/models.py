from django.db import models
from django.contrib.auth.models import AbstractUser
from Restaurant.models              import Restaurant
# Create your models here.
class User(AbstractUser):
    pass

class Wishlist(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta():
        db_table        = "wishlists"
        unique_together = ['user', 'restaurant']

class Review(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    content    = models.TextField()
    rating     = models.IntegerField()

    class Meta():
        db_table = "reviews"