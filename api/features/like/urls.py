from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.like.views import LikeViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', LikeViewSet.as_view({'post': 'create'})),
    path('<pk>', LikeViewSet.as_view({'delete': 'destroy'})),
] + router.urls
