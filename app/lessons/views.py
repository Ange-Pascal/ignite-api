from rest_framework.viewsets import ModelViewSet
from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from lessons.permissions import IsAdminOrInstructor
from rest_framework.permissions import IsAuthenticated

class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]
