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

    def get_queryset(self):
        user = self.request.user

        # Admin peut voir toutes les vidéos
        if user.roles.filter(name="admin").exists():
            return Video.objects.all()

        # Instructeur : seulement ses vidéos
        if user.roles.filter(name="instructor").exists():
            return Video.objects.filter(
                lesson__module__course__user=user
            )

        # Tout le monde d'autre : aucune vidéo
        return Video.objects.none()
