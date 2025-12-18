from rest_framework.viewsets import ModelViewSet
from courses.models import Course
from courses.serializers import CourseSerializer
from courses.permissions import CoursePermission


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
