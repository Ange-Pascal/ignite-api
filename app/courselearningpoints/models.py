from django.db import models
from courses.models import Course

class CourseLearningPoint(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="learning_points",
        on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255)

    class Meta:
        # On garde l'ordre d'insertion pour l'affichage
        ordering = ['id']

    def __str__(self):
        return f"{self.course.title} - {self.content}"
