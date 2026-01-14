from django.db import models
from quizquestions.models import QuizQuestion
from quizoptions.models import QuizOption
from quizattempts.models import QuizAttempt

class QuizAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    selected_option = models.ForeignKey(
        QuizOption,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="answers"
    )
    answer_text = models.TextField(blank=True, null=True)
    uploaded_file = models.FileField(
        upload_to="quiz_answers/",
        blank=True,
        null=True
    )
    is_correct = models.BooleanField(null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Answer by {self.attempt.user.email} for {self.question.text}"
