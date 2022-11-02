from django.db import models
from .choice import CATEGORY_CHOICES
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, Thumbnail
import os
from django.conf import settings
class Restaurant(models.Model):
    name = models.CharField(max_length=20) # 가게 이름
    address = models.CharField(max_length=200, unique=True) # 가게 주소
    phone_number=models.CharField(max_length=64, verbose_name='전화') # 가게 전화
    #업종 (ex: 양식, 중식, 한식)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=18, verbose_name='분류')
    #메뉴
    menu=models.TextField()
    #평점?
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(500, 350)],
        format="JPEG",
        options={"quality": 80},
    )
    thumbnail = ImageSpecField(
        source="image",
        processors=[Thumbnail(300, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
            os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail.path))
        super(Restaurant, self).delete(*args, **kargs)