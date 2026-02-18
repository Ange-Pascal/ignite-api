from django.db import models

from courses.models import Course


class CourseRequirement(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="requirements_list",
        on_delete=models.CASCADE
    )

    experience = models.CharField(
        max_length=255,
        help_text="Maitriser les bases de l'html/css"
    )

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
        verbose_name = "Prérequis du cours"
        verbose_name_plural = "Prérequis des cours"

    def __str__(self):
        return f"{self.course.title} - {self.experience}"
