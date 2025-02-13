import json
import uuid

from django.conf import settings
from django.core.cache import cache
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer

from api.features.models import Follow, Post


class MessageConsumer:
    def __init__(self, topics):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=settings.KAFKA_HOSTS,
            group_id=settings.KAFKA_GROUP_ID,
            auto_offset_reset='latest',
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.topic_handlers = {
            "es": self.send_elasticsearch,
            "post": self.update_post_cache
        }

    def update_post_cache(*args, data=None, **kwargs):
        try:
            follows = Follow.objects.filter(follower=uuid.UUID(data))
            if follows.count() < 1000:
                for follow in follows:
                    followee_users = list(
                        Follow.objects.filter(follower=follow.followee).values_list('followee', flat=True))
                    newsfeed_ids = list(Post.objects.filter(user__in=followee_users).values_list('id', flat=True))
                    cache.set(f'newsfeeds_{follow.followee.pk}', newsfeed_ids)
            print(f"Update post cache: {data}")
        except Exception as e:
            print(e)

    def send_elasticsearch(self, data=None, *args, **kwargs):
        es = Elasticsearch(settings.ELASTICSEARCH_HOSTS)
        es.index(index='posts', document=data)
        print(f"Sent to Elasticsearch: {data}")

    def consume_messages(self):
        print(f"Listening to kafka topic: {self.consumer.subscription()}")
        try:
            for message in self.consumer:
                topic = message.topic
                data = message.value
                handler = self.topic_handlers.get(topic)
                if handler:
                    print(f"Message received: {message.value}")
                    handler(data=data)
                    self.consumer.commit()
        except Exception as e:
            print(f"Kafka Consumer Error: {e}")
        finally:
            self.consumer.close()
