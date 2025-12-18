from rest_framework.routers import DefaultRouter
from outcomes.views import OutcomeViewSet

router = DefaultRouter()
router.register(r"outcomes", OutcomeViewSet, basename="outcome")

urlpatterns = router.urls
