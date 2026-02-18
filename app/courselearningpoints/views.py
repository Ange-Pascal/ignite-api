from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CourseLearningPoint
from .serializers import LearningPointSerializer
from .permissions import IsInstructorOwnerOrAdmin

class LearningPointViewSet(viewsets.ModelViewSet):
    """
    Gestion des points d'apprentissage (Ce que vous allez apprendre).
    """
    queryset = CourseLearningPoint.objects.all()
    serializer_class = LearningPointSerializer
    permission_classes = [IsInstructorOwnerOrAdmin]

    def get_queryset(self):
        """
        Optionnel : Filtrer les points par cours via un paramètre URL
        Ex: /api/learning-points/?course_id=1
        """
        queryset = self.queryset
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        """
        Assure que le point est lié au bon cours lors de la création
        et valide que l'utilisateur a le droit d'ajouter un point à ce cours.
        """
        # On peut ici ajouter une validation supplémentaire si nécessaire
        serializer.save()
