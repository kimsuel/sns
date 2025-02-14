from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.bookmark.views import BookmarkViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('bookmarks', BookmarkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('bookmarks/<pk>', BookmarkViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
]
