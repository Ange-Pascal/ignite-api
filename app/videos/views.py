from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Video
from .serializers import VideoSerializer
from .permissions import VideoPermission

class VideoViewSet(ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, VideoPermission]
    parser_classes = [MultiPartParser, FormParser]

