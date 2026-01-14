from django.db import models
from quizs.models import Quiz
from users.models import User
from django.conf import settings



class QuizAttempt(models.Model):
    STATUS_CHOICES = [
        ("in_progress", "In progress"),
        ("submitted", "Submitted"),
        ("passed", "Passed"),
        ("failed", "Failed"),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts"
    )

    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress"
    )

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
        ordering = ["-started_at"]
        unique_together = ["quiz", "user", "started_at"]

    def __str__(self):
        return f"{self.user} - {self.quiz.title} ({self.status})"

