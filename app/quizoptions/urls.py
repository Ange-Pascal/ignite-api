from rest_framework.routers import DefaultRouter
from .views import QuizOptionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(
    r"quiz-options",
    QuizOptionViewSet,
    basename="quiz-option"
)

urlpatterns = [
    path("", include(router.urls)),  # <- wrap le router dans une liste et include()
]
