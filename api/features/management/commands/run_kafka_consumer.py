import threading

from django.core.management import BaseCommand

from common.kafka.consumer import MessageConsumer


class Command(BaseCommand):
    help = "Run Kafka Consumer to process messages"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Kafka Consumer started"))
        topics = ['es', 'post']
        consumer = MessageConsumer(topics=topics)
        consumer.consume_messages()
