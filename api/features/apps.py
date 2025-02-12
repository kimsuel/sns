import threading
import os
import django
from django.apps import AppConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sns.settings')
# django.setup()


class FeatureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.features'

    def ready(self):
        from common.kafka.consumer import MessageConsumer

        topics = ['es', 'post']
        consumer = MessageConsumer(topics=topics)

        thread = threading.Thread(target=consumer.consume_messages, daemon=True)
        thread.start()
