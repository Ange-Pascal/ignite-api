from rest_framework import serializers
from .models import QuizQuestion
from quizs.models import Quiz
from typequestions.models import TypeQuestion


class QuizQuestionSerializer(serializers.ModelSerializer):
    quiz_id = serializers.PrimaryKeyRelatedField(
        queryset = Quiz.objects.all(),
        source = "quiz",
        write_only = True
    )


    type_question_id = serializers.PrimaryKeyRelatedField(
        queryset = TypeQuestion.objects.all(),
        source = "type_question"
    )

    class Meta:
        model = QuizQuestion
        fields = [
            "id",
            "quiz_id",
            "question_text",
            "type_question_id",
            "points",
            "order"
        ]

        read_only_fields = ["id"]
