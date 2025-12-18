# outcomes/models.py
from django.db import models
from courses.models import Course

class Outcome(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="outcomes",
        on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.title} - {self.label}"
