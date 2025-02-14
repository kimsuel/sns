from django.db import models

from api.features.post.models import Post
from api.user.models import User
from common.models import TimeStampedModel


class Bookmark(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks')
