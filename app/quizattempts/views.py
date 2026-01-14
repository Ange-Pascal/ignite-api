from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import QuizAttempt
from quizs.models import  Quiz
from .serializers import QuizAttemptSerializer
from .permissions import IsStudentOrAdminForQuizAttempt


class QuizAttemptViewSet(viewsets.ModelViewSet):
    """
    Gestion des QuizAttempts (tentatives de quiz)
    """

    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated, IsStudentOrAdminForQuizAttempt]
    queryset = QuizAttempt.objects.none()  # nécessaire pour Swagger / DRF schema

    def get_queryset(self):
        user = self.request.user
        roles = list(user.roles.values_list("name", flat=True))

        # Admin : voir toutes les tentatives
        if user.is_staff or "admin" in roles:
            return QuizAttempt.objects.all()

        # Student : voir uniquement ses tentatives
        if "student" in roles:
            return QuizAttempt.objects.filter(user=user)

        # Autres : aucun accès
        return QuizAttempt.objects.none()

    @action(
        detail=False,
        methods=["post"],
        url_path="start_quiz",
        permission_classes=[IsAuthenticated, IsStudentOrAdminForQuizAttempt]
    )
    def start_quiz(self, request):
        """
        Lancer un quiz et créer un QuizAttempt.
        Seul un student ou admin peut créer.
        """
        # Vérifie explicitement les permissions avant de continuer
        self.check_permissions(request)


        quiz_id = request.data.get("quiz_id")

        if not quiz_id:
            return Response(
                {"detail": "quiz_id est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        quiz = get_object_or_404(Quiz, pk=quiz_id)
        user = request.user

        # La permission IsStudentOrAdminForQuizAttempt garantit que seuls
        # les students (ou admin) passent cette étape, donc pas besoin de vérif manuelle ici

        # Vérifier s’il existe déjà une tentative in_progress
        existing_attempt = QuizAttempt.objects.filter(
            quiz=quiz, user=user, status="in_progress"
        ).first()
        if existing_attempt:
            serializer = QuizAttemptSerializer(existing_attempt)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Créer une nouvelle tentative
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            user=user,
            status="in_progress",
            started_at=timezone.now()
        )
        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
