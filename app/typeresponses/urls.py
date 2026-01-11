from rest_framework.routers import DefaultRouter
from .views import TypeResponseViewSet

router = DefaultRouter()
router.register(
    "type-responses",
    TypeResponseViewSet,
    basename="type-response"
)

urlpatterns = router.urls
