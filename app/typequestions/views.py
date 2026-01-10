from rest_framework.viewsets import ModelViewSet
from .models import TypeQuestion
from .serializers import TypeQuestionSerializer
from .permissions import TypeQuestionPermission

class TypeQuestionViewSet(ModelViewSet):
    queryset = TypeQuestion.objects.all()
    serializer_class = TypeQuestionSerializer
    permission_classes = [TypeQuestionPermission]
