from rest_framework import serializers
from .models import Quiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "type_quiz",
            "passing_score",
            "max_attempts",
            "time_limit",
            "shuffle_questions",
            "shuffle_options",
            "status",
            "quizable_type",
            "quizable_id",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user

        return super().create(validated_data)

