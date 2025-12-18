# reviews/models.py
from django.db import models
from courses.models import Course
from users.models import User

class Review(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course", "user")  # un utilisateur ne peut noter un cours qu'une fois
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.course.title} ({self.rating})"
