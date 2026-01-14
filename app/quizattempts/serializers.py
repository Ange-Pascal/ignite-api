from rest_framework import serializers
from .models import QuizAttempt

class QuizAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer pour QuizAttempt
    - Lecture : inclut tous les champs importants
    - Création : l'utilisateur connecté est automatiquement assigné
    """

    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "quiz",
            "user",
            "started_at",
            "submitted_at",
            "score",
            "status",
        ]
        read_only_fields = [
            "id",
            "user",
            "started_at",
            "submitted_at",
            "score",
            "status",
        ]

    def create(self, validated_data):
        """
        Crée une tentative et associe automatiquement l'utilisateur connecté
        """
        user = self.context["request"].user
        return QuizAttempt.objects.create(user=user, **validated_data)
