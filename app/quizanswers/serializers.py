from rest_framework import serializers
from .models import QuizAnswer

class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = [
            "id",
            "attempt",
            "question",
            "selected_option",
            "answer_text",
            "uploaded_file",
            "is_correct",
        ]
        read_only_fields = ["is_correct"]
