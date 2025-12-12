from rest_framework import viewsets, permissions
from instructors.models import InstructorProfile
from instructors.serializers import InstructorProfileSerializer
from instructors.permissions import IsInstructorAndOwnerOrAdmin
from rest_framework.exceptions import ValidationError




class InstructorProfileView(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorAndOwnerOrAdmin]


    def perform_create(self, serializer):
        if InstructorProfile.objects.filter(user=self.request.user).exists():
            raise ValidationError("Vous avez déjà un profil.")
        serializer.save(user=self.request.user)
