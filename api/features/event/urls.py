from rest_framework.routers import DefaultRouter

from api.features.event.views import EventViewSet

router = DefaultRouter(trailing_slash=False)
router.register('events', EventViewSet)


urlpatterns = [

]