from rest_framework import serializers
from instructors.models import InstructorProfile

class InstructorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorProfile
        fields = ["id", "user", "bio", "experience", "links"]
        read_only_fields = ["id", "user"]
