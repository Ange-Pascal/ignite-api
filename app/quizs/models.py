from django.db import models
from typequizs.models import TypeQuiz
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Quiz(models.Model):
    """
    Règles, paramètres et relations dans le model quiz
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        PUBLISHED = "published", "Publié"
        ARCHIVED = "archived", "Archivé"

    type_quiz = models.ForeignKey(
        TypeQuiz,
        on_delete=models.PROTECT,
        related_name="quizzes"
    )
    # Infos de la table

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Règles

    passing_score = models.PositiveBigIntegerField()
    max_attempts = models.PositiveBigIntegerField(default=1)
    time_limit = models.PositiveBigIntegerField(
        null=True, blank=True, help_text="Durée en minute"
    )

    # Options

    shuffle_questions = models.BooleanField(default=False)
    shuffle_options = models.BooleanField(default=False)


    # Polimorphisme (Course & Module)
    quizable_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    quizable_id = models.PositiveIntegerField()
    quizable = GenericForeignKey("quizable_type", "quizable_id")

    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    # Auteur du quiz

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )
    # meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

