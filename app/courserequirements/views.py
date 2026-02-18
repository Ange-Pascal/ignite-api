from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from .models import CourseRequirement
from .serializers import CourseRequirementSerializer
from .permissions import IsAdminOrCourseOwner # Import de ta nouvelle classe

class CourseRequirementViewSet(ModelViewSet):
    queryset = CourseRequirement.objects.all()
    serializer_class = CourseRequirementSerializer
    permission_classes = [IsAdminOrCourseOwner]

    def perform_create(self, serializer):
        # Sécurité supplémentaire : On vérifie que celui qui crée le prérequis
        # est bien le proprio du cours ou un admin
        course = serializer.validated_data['course']
        is_admin = self.request.user.roles.filter(name="admin").exists()

        if course.user != self.request.user and not is_admin:
            raise PermissionDenied("Vous n'êtes pas le propriétaire de ce cours.")

        serializer.save()

    def get_queryset(self):
        # Optimisation : On ajoute select_related pour éviter les requêtes inutiles sur le cours
        queryset = CourseRequirement.objects.select_related('course').all()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

