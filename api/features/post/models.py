from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from api.user.models import User
from common.models import TimeStampedModel


class Post(ExportModelOperationsMixin('post'), TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(blank=True, null=True)


class Image(ExportModelOperationsMixin('image'), TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=255, blank=True)
