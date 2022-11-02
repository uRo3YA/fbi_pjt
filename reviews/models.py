from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.
'''
게시판 기능 
- 제목(20글자이내)
- 내용(긴 글)
- 글 작성시간/수정시간(자동으로 기록, 날짜/시간)
'''
# 1. 모델 설계 (DB 스키마 설계)
from django.conf import settings

class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_revies')
    Restaurant= models.ForeignKey('Restaurant.Restaurant', on_delete=models.CASCADE)
                            
class Comment(models.Model):
    # post = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name='게시글')
    # writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='댓글작성자')
    # # writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, verbose_name='댓글작성자')
    # # writer = models.CharField(max_length=17, null=True, verbose_name='댓글작성자')
    # content = models.TextField(verbose_name='댓글내용')
    # created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    # deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    # reply = models.IntegerField(verbose_name='답글위치', default=0)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.content

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + '일 전'
        else:
            return False 

    class Meta:
        db_table = '댓글'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'