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
    FollowingSerializer,
)

from common.viewsets import MappingViewSetMixin


class PostViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    serializer_action_classes = {
        'list': PostReadSerializer,
        'retrieve': PostReadSerializer,
        'user_posts': PostReadSerializer
    }

    def user_posts(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=self.kwargs['user_id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post_comments(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['post_id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FollowViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    serializer_action_classes = {
        'followers': FollowerSerializer,
        'followings': FollowingSerializer,
    }

    def followers(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(follower=self.kwargs['follower_id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def followings(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(following=self.kwargs['following_id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    serializer_action_classes = {
        'list': BookmarkReadSerializer,
        'retrieve': BookmarkReadSerializer,
        'user_bookmarks': BookmarkReadSerializer
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def user_bookmarks(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=self.kwargs['user_id'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
