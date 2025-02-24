from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.features.event.models import Event
from api.features.event.serializers import EventSerializer, EventReadSerializer
from common.viewsets import MappingViewSetMixin


class EventViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Event.objects.prefetch_related('tickets')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name',)
    serializer_class = EventSerializer
    serializer_action_classes = {
        'retrieve': EventReadSerializer,
    }
