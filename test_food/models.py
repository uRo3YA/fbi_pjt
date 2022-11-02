from django.db import models

# Create your models here.
class Store(models.Model):
#         store_id=
        title=models.CharField(max_length=255)
        addr=models.CharField(max_length=255)
        longtitude= models.FloatField()
        latitude= models.FloatField()
        tel= models.CharField(max_length=20)
        category=models.CharField(max_length=20)