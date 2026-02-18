from rest_framework.routers import DefaultRouter
from .views import CourseRequirementViewSet

router = DefaultRouter()
router.register("requirements", CourseRequirementViewSet, basename="requirements")

urlpatterns = router.urls

