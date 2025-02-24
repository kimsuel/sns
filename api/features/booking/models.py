from django.db import models

from api.user.models import User
from common.models import TimeStampedModel


class Booking(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    payment = models.CharField(max_length=20, help_text='결제 수단')
