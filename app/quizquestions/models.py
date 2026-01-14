from django.db import models
from quizs.models import Quiz
from typequestions.models import TypeQuestion



class QuizQuestion(models.Model):
    """
    Docstring pour QuizQuestion
    """

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="quiz"
    )

    type_question = models.ForeignKey(
        TypeQuestion,
        on_delete=models.CASCADE,
        related_name="typequestion"
    )

    question_text = models.TextField()
    points = models.PositiveBigIntegerField(default=1)

    order = models.PositiveIntegerField(
        help_text="Ordre d'affichage dans le quiz"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["order"]
        unique_together = ["quiz", "order"]
        verbose_name = "Quiz Question"
        verbose_name_plural = "Quiz Questions"

    def __str__(self):
        return f"Q{self.order} - {self.question_text[:50]}"

