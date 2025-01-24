from django.core import serializers
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.features.models import Post, Comment, Like, Follow, Bookmark
from api.features.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowSerializer,
    BookmarkSerializer,
    PostReadSerializer,
    BookmarkReadSerializer,
    FollowerSerializer,
    FolloweeSerializer,
    SimpleBookmarkSerializer,
    PostCreateSerializer,
    PostImageUpdateSerializer,
)
from common.viewsets import MappingViewSetMixin


class PostViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('images')
    serializer_class = PostSerializer
    serializer_action_classes = {
        'create': PostCreateSerializer,
        'add_newsfeed_images': PostImageUpdateSerializer,
        'list': PostReadSerializer,
        'retrieve': PostReadSerializer,
        'timeline_posts': PostReadSerializer,
        'newsfeed_posts': PostReadSerializer
    }

    def timeline_posts(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=self.request.user)
        return self.handle_paginated_response(queryset)

    def newsfeed_posts(self, request, *args, **kwargs):
        followee_users = cache.get(f'followee_user_{self.request.user.pk}')
        if not followee_users:
            followee_users = list(Follow.objects.filter(follower=self.request.user
                                                        ).values_list('followee', flat=True))
            cache.set(f'followee_user_{self.request.user.pk}', followee_users)

        newsfeed_ids = cache.get(f'newsfeeds_{self.request.user.pk}')
        if not newsfeed_ids:
            newsfeed_ids = list(self.get_queryset().filter(user__in=followee_users).values_list('id', flat=True))
            cache.set(f'newsfeeds_{self.request.user.pk}', newsfeed_ids)

        queryset = self.get_queryset().filter(id__in=newsfeed_ids).order_by('-created_at')
        return self.handle_paginated_response(queryset)

    def add_newsfeed_images(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CommentViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post_comments(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['post_id'])
        return self.handle_paginated_response(queryset)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FollowViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    serializer_action_classes = {
        'followers': FollowerSerializer,
        'followees': FolloweeSerializer,
    }

    def followers(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(follower=self.kwargs['follower_id'])
        return self.handle_paginated_response(queryset)

    def followees(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(followee=self.kwargs['followee_id'])
        return self.handle_paginated_response(queryset)


class BookmarkViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    serializer_action_classes = {
        'list': SimpleBookmarkSerializer,
        'retrieve': BookmarkReadSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
