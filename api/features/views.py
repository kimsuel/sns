from django.core.cache import cache
from django.db.models import Count
from django.http import JsonResponse
from django_elasticsearch_dsl.search import Search
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets

from api.features.filters import PostFilter
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
from api.user.models import User
from common.viewsets import MappingViewSetMixin


class PostViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('images')
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
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
        user = self.request.user

        newsfeed_ids = cache.get(f'newsfeeds_{user.pk}')
        if newsfeed_ids:
            celeb_users = User.objects.filter(
                followee__follower=user).annotate(
                follower_count=Count('follower')
            ).filter(follower_count__gte=1000).values_list('id', flat=True)
            if celeb_users:
                celeb_newsfeed_ids = list(self.get_queryset().filter(user__in=celeb_users).values_list('id', flat=True))
                newsfeed_ids = list(set(newsfeed_ids + celeb_newsfeed_ids))
                cache.set(f'newsfeeds_{user.pk}', newsfeed_ids)
        else:
            followee_users = Follow.objects.filter(follower=user).values_list('followee', flat=True)
            newsfeed_ids = list(self.get_queryset().filter(user__in=followee_users).values_list('id', flat=True))
            cache.set(f'newsfeeds_{user.pk}', newsfeed_ids)

        queryset = self.get_queryset().filter(id__in=newsfeed_ids).order_by('-created_at')
        return self.handle_paginated_response(queryset)

    def add_newsfeed_images(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def search_posts(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        search = Search(index='posts').query('match', name=query)
        response = search.execute()
        results = [{'text': hit.text} for hit in response]
        return JsonResponse(results, safe=False)


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
