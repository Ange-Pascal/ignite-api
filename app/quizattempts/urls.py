from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizAttemptViewSet

router = DefaultRouter()
router.register(r'quiz-attempts', QuizAttemptViewSet, basename='quiz-attempt')

urlpatterns = [
    # Routes CRUD + route custom start_quiz
    path('', include(router.urls)),
]
