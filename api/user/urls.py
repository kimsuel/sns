from django.urls import path
from rest_framework.routers import DefaultRouter

from api.user.views import RegisterViewSet, AuthViewSet, UserViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('signup', RegisterViewSet.as_view({'post': 'create'}), name='signup'),
    path('login', AuthViewSet.as_view({'post': 'create'}), name='login'),
    path('<uuid:pk>', UserViewSet.as_view({'get': 'retrieve', 'put': 'partial_update'}), name='user'),
] + router.urls
