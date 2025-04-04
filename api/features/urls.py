from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('bookmarks/', include('api.features.bookmark.urls')),
    path('comments/', include('api.features.comment.urls')),
    path('follows/', include('api.features.follow.urls')),
    path('likes/', include('api.features.like.urls')),
    path('posts/', include('api.features.post.urls')),
    path('bookings/', include('api.features.booking.urls')),
    path('tickets/', include('api.features.ticket.urls')),
    path('events/', include('api.features.event.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
