from django.db import models

from api.features.booking.models import Booking
from api.features.event.models import Event
from common.models import TimeStampedModel


class Ticket(TimeStampedModel):
    STATUS = [
        ('available', 'Available'),
        ('not-available', 'Not-available')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    price = models.PositiveIntegerField(default=0, help_text='티켓 가격')
    status = models.CharField(max_length=20, choices=STATUS, default='available', help_text='티켓 상태')
    seat = models.CharField(max_length=20, help_text='좌석명')
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
