from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('bookmark', include('api.features.bookmark.urls')),
    path('comment', include('api.features.comment.urls')),
    path('follow', include('api.features.follow.urls')),
    path('like', include('api.features.like.urls')),
    path('post', include('api.features.post.urls')),
] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
