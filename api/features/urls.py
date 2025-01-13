from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.views import PostViewSet, CommentViewSet, LikeViewSet, FollowViewSet, BookmarkViewSet

router = DefaultRouter(trailing_slash=False)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikeViewSet)
router.register('follows', FollowViewSet)
router.register('bookmark', BookmarkViewSet)

urlpatterns = [
    path('posts/<user>', PostViewSet.as_view({'get': 'user_posts'})),
] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
