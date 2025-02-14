from django.db import models
from api.user.models import User
from common.models import TimeStampedModel


class Follow(TimeStampedModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')

    class Meta:
        unique_together = ('follower', 'followee')
