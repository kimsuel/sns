from rest_framework.routers import DefaultRouter

from api.features.ticket.views import TicketViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', TicketViewSet)

urlpatterns = [] + router.urls