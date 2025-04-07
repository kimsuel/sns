from django.db import transaction
from django.db.utils import DatabaseError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            ticket_instances = []
            for ticket in tickets:
                try:
                    ticket = Ticket.objects.select_for_update().get(id=ticket)
                    if ticket.status != 'available':
                        raise ValidationError(f"티켓 ID {ticket}는 이미 예약되었습니다.")

                    ticket.status = 'not_available'
                    ticket.save()
                    ticket_instances.append(ticket)
                except DatabaseError:
                    raise ValidationError(f"티켓 ID {ticket}에 대한 동시 예약 시도가 감지되었습니다.")

            instance = super().create(validated_data)
        return instance