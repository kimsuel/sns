import json

from django.conf import settings
from django.core.cache import cache
from kafka import KafkaConsumer

from api.features.models import Follow, Post


class MessageConsumer:
    def __init__(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=settings.KAFKA_HOSTS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def update_post_cache(*args, user_id=None, **kwargs):
        follows = Follow.objects.filter(follower=user_id)
        if follows.count() < 1000:
            for follow in follows:
                followee_users = list(
                    Follow.objects.filter(follower=follow.followee).values_list('followee', flat=True))
                newsfeed_ids = list(Post.objects.filter(user__in=followee_users).values_list('id', flat=True))
                cache.set(f'newsfeeds_{follow.followee.pk}', newsfeed_ids)

    def consume_messages(self):
        print(f"Listening to kafka topic: {self.consumer.subscription()}")
        for message in self.consumer:
            data = message.value
            self.update_post_cache(user_id=data)
            print(f"Message received: {message.value}")
