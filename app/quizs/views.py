from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Quiz
from .serializers import QuizSerializer
from .permissions import IsAdminOrInstructorOwner

class QuizViewSet(ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructorOwner]

    def get_queryset(self):
        user = self.request.user
        user_roles = list(user.roles.values_list("name", flat=True))

        # Admin : tous les quiz
        if user.is_staff or "admin" in user_roles:
            return Quiz.objects.all()

        # Pour list : instructor voit seulement ses quiz, student ne voit rien
        if self.action == "list":
            if "instructor" in user_roles:
                return Quiz.objects.filter(created_by=user)
            else:  # student ou autres
                return Quiz.objects.none()

        # Pour retrieve/update/delete : renvoyer tous les quiz, permission décidera
        return Quiz.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
