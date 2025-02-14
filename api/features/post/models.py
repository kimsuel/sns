from django.db import models
from api.user.models import User
from common.models import TimeStampedModel


class Post(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(blank=True, null=True)


class Image(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=255, blank=True)
