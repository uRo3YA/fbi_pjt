from django.db import models
from .choice import CATEGORY_CHOICES

class Restaurant(models.Model):
    name = models.CharField(max_length=20) # 가게 이름
    address = models.CharField(max_length=200, unique=True) # 가게 주소
    phone_number=models.CharField(max_length=64, verbose_name='전화') # 가게 전화
    #업종 (ex: 양식, 중식, 한식)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=18, verbose_name='분류')
    #메뉴
    menu=models.TextField()
    #평점