from rest_framework import viewsets

from api.features.bookmark.models import Bookmark
from api.features.bookmark.serializers import (
    BookmarkSerializer,
    SimpleBookmarkSerializer,
    BookmarkReadSerializer
)
from common.viewsets import MappingViewSetMixin


class BookmarkViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    serializer_action_classes = {
        'list': SimpleBookmarkSerializer,
        'retrieve': BookmarkReadSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
