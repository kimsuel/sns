from rest_framework import viewsets

from api.features.comment.models import Comment
from api.features.comment.serializers import CommentSerializer
from common.viewsets import MappingViewSetMixin


class CommentViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post_comments(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['post_id'])
        return self.handle_paginated_response(queryset)
