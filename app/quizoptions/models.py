from django.db import models
from quizquestions.models import QuizQuestion
from typeresponses.models import TypeResponse


class QuizOption(models.Model):
    quiz_question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name="options"   # ✅ pluriel
    )

    type_response = models.ForeignKey(
        TypeResponse,
        on_delete=models.PROTECT,
        related_name="quiz_options"  # ✅ explicite
    )

    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Quiz Option"
        verbose_name_plural = "Quiz Options"

    def __str__(self):
        return f"Option({'✔' if self.is_correct else '✘'}) - {self.option_text[:40]}"
