# highlights/views.py
from rest_framework.viewsets import ModelViewSet
from highlights.models import Highlight
from highlights.serializers import HighlightSerializer
from highlights.permissions import IsAdminOrInstructor
from rest_framework.permissions import IsAuthenticated

class HighlightViewSet(ModelViewSet):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]
