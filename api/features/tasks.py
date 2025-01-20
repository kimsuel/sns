from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.cache import cache

from api.features.models import Follow, Post


@shared_task
def update_post_cache(*args, user_id=None, **kwargs):
    follows = Follow.objects.filter(follower=user_id)
    for follow in follows:
        following_users = list(Follow.objects.filter(follower=follow.following).values_list('following', flat=True))
        newsfeed_ids = list(Post.objects.filter(user__in=following_users).values_list('id', flat=True))
        cache.set(f'newsfeeds_{follow.following.pk}', newsfeed_ids)

    return True
