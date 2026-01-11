from rest_framework import serializers
from .models import TypeResponse

class TypeResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeResponse
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

