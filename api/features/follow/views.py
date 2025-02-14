from rest_framework import viewsets

from api.features.follow.models import Follow
from api.features.follow.serializers import (
    FollowSerializer,
    FollowerSerializer,
    FolloweeSerializer
)
from common.viewsets import MappingViewSetMixin


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
