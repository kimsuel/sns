from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('booking', BookingViewSet)
