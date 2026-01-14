from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from quizquestions.models import QuizQuestion
from quizquestions.serializers import QuizQuestionSerializer
from .permissions import IsAdminOrInstructorQuizQuestionOwner


class QuizQuestionViewSet(ModelViewSet):
    """
    ViewSet pour gérer les QuizQuestions

    - Admin : accès total
    - Instructor : CRUD uniquement sur les questions de ses propres quiz
    - Autres : aucun accès
    """

    serializer_class = QuizQuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructorQuizQuestionOwner]

    def get_queryset(self):
        """
        Filtrage du queryset selon rôle pour list/retrieve
        """
        user = self.request.user
        roles = list(user.roles.values_list("name", flat=True))

        # Admin : toutes les questions
        if user.is_staff or "admin" in roles:
            return QuizQuestion.objects.select_related("quiz", "type_question")

        # Instructor : uniquement ses quiz
        if "instructor" in roles:
            return QuizQuestion.objects.filter(
                quiz__created_by=user
            ).select_related("quiz", "type_question")

        # Autres : aucun accès
        return QuizQuestion.objects.none()

    def perform_create(self, serializer):
        """
        Création sécurisée selon rôle
        """
        quiz = serializer.validated_data["quiz"]
        user = self.request.user
        roles = list(user.roles.values_list("name", flat=True))

        if user.is_staff or "admin" in roles:
            serializer.save()
            return

        if "instructor" in roles:
            if quiz.created_by != user:
                raise PermissionDenied(
                    "Vous n'êtes pas autorisé à ajouter des questions à ce quiz."
                )
            serializer.save()
            return

        raise PermissionDenied("Vous n'êtes pas autorisé à créer une question.")

    def get_object(self):
        """
        Récupère l'objet et applique la permission explicitement
        pour renvoyer 403 au lieu de 404
        """
        # On récupère l'objet sans filtrer par queryset
        obj = get_object_or_404(QuizQuestion, pk=self.kwargs["pk"])

        # Vérifie les permissions sur l'objet
        self.check_object_permissions(self.request, obj)

        return obj
