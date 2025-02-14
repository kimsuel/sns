from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.follow.views import FollowViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('follows', FollowViewSet.as_view({'post': 'create'})),
    path('follows/follower/<follower_id>', FollowViewSet.as_view({'get': 'followers', 'delete': 'destroy'})),
    path('follows/followee/<followee_id>', FollowViewSet.as_view({'get': 'followees', 'delete': 'destroy'})),
]
