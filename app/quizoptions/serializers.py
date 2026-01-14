from rest_framework import serializers
from .models import QuizOption


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = [
            "id",
            "quiz_question",
            "type_response",
            "option_text",
            "is_correct",
        ]
        read_only_fields = ["id"]
