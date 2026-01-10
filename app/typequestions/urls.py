from rest_framework.routers import DefaultRouter
from .views import TypeQuestionViewSet

router = DefaultRouter()
router.register(
    "type-questions",
    TypeQuestionViewSet,
    basename="type-question"
)

urlpatterns = router.urls
