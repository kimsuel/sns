from django.db import transaction
from rest_framework import serializers

from api.features.booking.models import Booking
from api.features.ticket.models import Ticket


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        tickets = validated_data.pop('tickets')

        with transaction.atomic():
            for ticket in tickets:
                ticket = Ticket.objects.select_for_update().get(id=ticket)
                ticket.status = 'available'
                ticket.save()

            super().create(validated_data)
