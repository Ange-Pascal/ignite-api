from rest_framework.viewsets import ModelViewSet
from typeresponses.models import TypeResponse
from .serializers import TypeResponseSerializer
from .permissions import TypeResponsePermission

class TypeResponseViewSet(ModelViewSet):
    queryset = TypeResponse.objects.all()
    serializer_class = TypeResponseSerializer
    permission_classes = [TypeResponsePermission]
