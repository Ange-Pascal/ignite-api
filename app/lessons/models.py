# lessons/models.py
from django.db import models
from modules.models import Module

class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        related_name="lessons",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ["position"]
        unique_together = ("module", "position")

    def __str__(self):
        return f"{self.module.title} - {self.title}"
