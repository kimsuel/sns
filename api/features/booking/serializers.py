from django.db import transaction
from rest_framework import serializers

from api.features.booking.models import Booking
from api.features.ticket.models import Ticket


class BookingSerializer(serializers.ModelSerializer):
    tickets = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Booking
        fields = ['tickets', 'payment']

    def create(self, validated_data):
        tickets = validated_data.pop('tickets')
        user = self.context['request'].user
        validated_data['user'] = user

        with transaction.atomic():
            for ticket in tickets:
                ticket = Ticket.objects.select_for_update().get(id=ticket)
                ticket.status = 'not_available'
                ticket.save()

            instance = super().create(validated_data)
        return instance