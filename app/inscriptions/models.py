from django.db import models
from users.models import User
from courses.models import Course

class Inscription(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        related_name="inscriptions",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        related_name="inscriptions",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
