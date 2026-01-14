from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import QuizOption
from .serializers import QuizOptionSerializer
from .permissions import IsAdminOrInstructorOwner


class QuizOptionViewSet(ModelViewSet):
    """
    ViewSet pour gérer les options de quiz.

    - Admin : accès total
    - Instructor : uniquement ses quiz
    - Autres : aucun accès
    """

    serializer_class = QuizOptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructorOwner]

    # 🔴 OBLIGATOIRE pour drf-spectacular
    queryset = QuizOption.objects.all()

    def get_queryset(self):
        user = self.request.user

        if not user or not user.is_authenticated:
            return QuizOption.objects.none()

        if user.is_staff:
            return QuizOption.objects.all()

        if hasattr(user, "roles") and user.roles.filter(name="admin").exists():
            return QuizOption.objects.all()

        if hasattr(user, "roles") and user.roles.filter(name="instructor").exists():
            return QuizOption.objects.filter(
                quiz_question__quiz__created_by=user
            )

        return QuizOption.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        quiz_question = serializer.validated_data["quiz_question"]

        if user.is_staff:
            serializer.save()
            return

        if hasattr(user, "roles") and user.roles.filter(name="admin").exists():
            serializer.save()
            return

        if hasattr(user, "roles") and user.roles.filter(name="instructor").exists():
            if quiz_question.quiz.created_by != user:
                raise PermissionDenied(
                    "Vous ne pouvez pas ajouter une option à ce quiz"
                )
            serializer.save()
            return

        raise PermissionDenied("Accès refusé")
