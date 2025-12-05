from django.db import models
from django.contrib.auth import get_user_model

class InstructorProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="instructor_profile")
    bio = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    links = models.TextField(blank=True)

    def __str__(self):
        return f"Profile de {self.user.email}"
