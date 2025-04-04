from rest_framework import serializers

from api.features.event.models import Event
from api.features.ticket.serializers import TicketSerializer


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class EventReadSerializer(serializers.ModelSerializer):
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_tickets(self, obj):
        tickets = obj.tickets.filter(status='available')
        return TicketSerializer(tickets, many=True).data
