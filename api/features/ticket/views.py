from rest_framework import viewsets

from api.features.ticket.models import Ticket
from api.features.ticket.serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

