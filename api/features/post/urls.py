from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.features.post.views import PostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', PostViewSet)

urlpatterns = [
    path('newsfeed', PostViewSet.as_view({'get': 'newsfeed_posts'})),
    path('timeline', PostViewSet.as_view({'get': 'timeline_posts'})),
    path('search', PostViewSet.as_view({'get': 'search_posts'}), name='search_posts'),
    path('newsfeed/images/<pk>', PostViewSet.as_view({'put': 'add_newsfeed_images'})),
] + router.urls
