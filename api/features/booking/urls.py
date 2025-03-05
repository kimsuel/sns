from rest_framework.routers import DefaultRouter

from api.features.booking.views import BookingViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', BookingViewSet)

urlpatterns = [] + router.urls
