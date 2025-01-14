from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.views import PostViewSet, CommentViewSet, LikeViewSet, FollowViewSet, BookmarkViewSet

router = DefaultRouter(trailing_slash=False)
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('posts/user/<user_id>', PostViewSet.as_view({'get': 'user_posts'})),
    path('comments/post/<post_id>', CommentViewSet.as_view({'get': 'post_comments'})),
    path('likes', LikeViewSet.as_view({'post': 'create'})),
    path('likes/<pk>', LikeViewSet.as_view({'delete': 'destroy'})),
    path('bookmarks', BookmarkViewSet.as_view({'post': 'create'})),
    path('bookmarks/user/<user_id>', BookmarkViewSet.as_view({'get': 'user_bookmarks', 'delete': 'destroy'})),
    path('follows', FollowViewSet.as_view({'post': 'create'})),
    path('follows/follower/<follower_id>', FollowViewSet.as_view({'get': 'followers', 'delete': 'destroy'})),
    path('follows/following/<following_id>', FollowViewSet.as_view({'get': 'followings', 'delete': 'destroy'})),
] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
