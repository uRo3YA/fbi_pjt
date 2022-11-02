from django.db import models
from .choice import CATEGORY_CHOICES
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill, Thumbnail
import os
from django.conf import settings
class Restaurant(models.Model):
    title=models.CharField(max_length=255)
    addr=models.CharField(max_length=255)
    longtitude= models.FloatField()
    latitude= models.FloatField()
    tel= models.CharField(max_length=20)
    category=models.CharField(max_length=20)
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