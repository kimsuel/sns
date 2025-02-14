from rest_framework import viewsets

from api.features.like.models import Like
from api.features.like.serializers import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
