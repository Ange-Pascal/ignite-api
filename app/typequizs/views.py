from rest_framework.viewsets import ModelViewSet
from .models import TypeQuiz
from .serializers import TypeQuizSerializer
from .permissions import TypeQuizPermission

class TypeQuizViewSet(ModelViewSet):
    queryset = TypeQuiz.objects.all()
    serializer_class = TypeQuizSerializer
    permission_classes = [TypeQuizPermission]
