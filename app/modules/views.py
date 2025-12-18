# modules/views.py
from rest_framework.viewsets import ModelViewSet
from modules.models import Module
from modules.serializers import ModuleSerializer
from modules.permissions import IsAdminOrInstructor
from rest_framework.permissions import IsAuthenticated

class ModuleViewSet(ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]
