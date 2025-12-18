# modules/models.py
from django.db import models
from courses.models import Course

class Module(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ["position"]
        unique_together = ("course", "position")

    def __str__(self):
        return f"{self.course.title} - {self.title}"
