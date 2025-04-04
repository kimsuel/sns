import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sns.settings")
django.setup()

from api.features.event.models import Event
from api.features.ticket.models import Ticket


class MockData:
    def __init__(self):
        self.create_event_and_tickets()

    @staticmethod
    def create_event_and_tickets():
        seat_types = [
            {'type': 'VIP석', 'price': 200000, 'count': 100},
            {'type': 'R석', 'price': 120000, 'count': 200},
            {'type': 'S석', 'price': 80000, 'count': 300},
            {'type': 'A석', 'price': 60000, 'count': 400}
        ]

        tickets_to_create = []

        for i in range(20):
            event = Event.objects.create(
                name=f'티켓 이벤트 {i}',
                description=f'티켓 이벤트 테스트를 위한 description {i}',
                seat_capacity=1000
            )

            for seat_info in seat_types:
                for _ in range(seat_info['count']):
                    ticket_data = {
                        'event': event,
                        'price': seat_info['price'],
                        'seat': seat_info['type']
                    }
                    tickets_to_create.append(Ticket(**ticket_data))

            if tickets_to_create:
                Ticket.objects.bulk_create(tickets_to_create, batch_size=100)
                tickets_to_create = []

MockData()
