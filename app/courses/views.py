from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from courses.models import Course
from courses.serializers import CourseSerializer
from courses.permissions import CoursePermission
from rest_framework.views import APIView


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CoursePermission]

    lookup_field = "slug"  # ⭐ clé du changement

    def perform_create(self, serializer):
        if self.request.user.roles.filter(name="instructor").exists():
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class CourseMetaDataView(APIView):
    """
    Expose les constantes du modèle Course pour le Frontend.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "levels": [
                {"value": value, "label": label}
                for value, label in Course.LEVEL_CHOICES
            ],
            "status": [
                {"value": value, "label": label}
                for value, label in Course.STATUS_CHOICES
            ],
            "languages": [
                {"value": value, "label": label}
                for value, label in Course.LANGUAGE_CHOICES
            ],
        }
        return Response(data)

