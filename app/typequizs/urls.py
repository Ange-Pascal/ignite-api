from rest_framework.routers import DefaultRouter
from .views import TypeQuizViewSet

router = DefaultRouter()
router.register(
    "type-quizzes",
    TypeQuizViewSet,
    basename="type-quiz"
)

urlpatterns = router.urls
