from django.db import models
from courses.models import Course

class Highlight(models.Model):
    TYPE_CHOICES = [
        ("badge", "Badge"),
        ("text", "Text"),
    ]

    course = models.ForeignKey(
        Course,
        related_name="highlights",
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.course.title} - {self.label} ({self.type})"
