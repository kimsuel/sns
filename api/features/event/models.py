from django.db import models

from common.models import TimeStampedModel


class Event(TimeStampedModel):
    name = models.CharField(max_length=125, help_text='이벤트명')
    description = models.TextField(blank=True, null=True, help_text='설명')
    seat_capacity = models.PositiveIntegerField(default=0, help_text='총 좌석수')
