from rest_framework.routers import DefaultRouter
from .views import LearningPointViewSet

router = DefaultRouter()
router.register("learningpoints", LearningPointViewSet, basename="learningpoints")

urlpatterns = router.urls

