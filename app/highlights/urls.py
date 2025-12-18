from rest_framework.routers import DefaultRouter
from highlights.views import HighlightViewSet

router = DefaultRouter()
router.register(r"highlights", HighlightViewSet, basename="highlight")

urlpatterns = router.urls
