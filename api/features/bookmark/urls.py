from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.bookmark.views import BookmarkViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', BookmarkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<pk>', BookmarkViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
] + router.urls
