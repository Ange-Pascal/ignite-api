from rest_framework import viewsets, permissions
from instructors.models import InstructorProfile
from instructors.serializers import InstructorProfileSerializer
from instructors.permissions import IsOwnerOrAdmin

class InstructorProfileView(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
