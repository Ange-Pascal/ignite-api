from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizQuestionViewSet

# Création du router DRF
router = DefaultRouter()
router.register(r'quiz-questions', QuizQuestionViewSet, basename='quiz-question')

urlpatterns = [
    path('', include(router.urls)),
]
