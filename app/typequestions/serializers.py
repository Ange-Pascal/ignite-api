from rest_framework import serializers
from .models import TypeQuestion

class TypeQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeQuestion
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

