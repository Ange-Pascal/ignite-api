from rest_framework import serializers
from .models import TypeQuiz

class TypeQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeQuiz
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

