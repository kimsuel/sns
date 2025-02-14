from django.urls import path
from rest_framework.routers import DefaultRouter

from api.features.comment.views import CommentViewSet

router = DefaultRouter(trailing_slash=False)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('comments/post/<post_id>', CommentViewSet.as_view({'get': 'post_comments'})),
]
