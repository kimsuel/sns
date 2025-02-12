import json

from django.conf import settings
from kafka import KafkaProducer


class MessageProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_HOSTS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )

    def send(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()
        print(f"Send message : {message}")
