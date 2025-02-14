from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.post.views import PostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/newsfeed', PostViewSet.as_view({'get': 'newsfeed_posts'})),
    path('posts/timeline', PostViewSet.as_view({'get': 'timeline_posts'})),
    path('posts/search', PostViewSet.as_view({'get': 'search_posts'}), name='search_posts'),
    path('posts/newsfeed/images/<pk>', PostViewSet.as_view({'put': 'add_newsfeed_images'})),
]
