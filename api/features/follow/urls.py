from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.follow.views import FollowViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', FollowViewSet.as_view({'post': 'create'})),
    path('follower/<follower_id>', FollowViewSet.as_view({'get': 'followers', 'delete': 'destroy'})),
    path('followee/<followee_id>', FollowViewSet.as_view({'get': 'followees', 'delete': 'destroy'})),
] + router.urls
