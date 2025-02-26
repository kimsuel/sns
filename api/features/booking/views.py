from rest_framework import viewsets

from api.features.booking.models import Booking
from api.features.booking.serializers import BookingSerializer
from common.viewsets import MappingViewSetMixin


class BookingViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
