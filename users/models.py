from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.
class User(AbstractUser):
    # description = models.TextField(blank=True)
    # nickname = models.CharField(max_length=40, blank=True)
    # image = ProcessedImageField(
    #     upload_to="images/",
    #     blank=True,
    #     processors=[Thumbnail(200, 200)],
    #     format="JPEG",
    #     options={"quality": 80},
    # )
    @property
    def full_name(self):
        return f'{self.last_name}{self.first_name}'



class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = ProcessedImageField(
        blank=True,
        processors=[Thumbnail(200, 200)],
        format="JPEG",
        options={"quality": 50},
    )

