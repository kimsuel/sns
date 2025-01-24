from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.cache import cache

from api.features.models import Follow, Post


@shared_task
def update_post_cache(*args, user_id=None, **kwargs):
    follows = Follow.objects.filter(follower=user_id)
    for follow in follows:
        followee_users = list(Follow.objects.filter(follower=follow.followee).values_list('followee', flat=True))
        newsfeed_ids = list(Post.objects.filter(user__in=followee_users).values_list('id', flat=True))
        cache.set(f'newsfeeds_{follow.followee.pk}', newsfeed_ids)

    return True
