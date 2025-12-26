from django.db import models
from lessons.models import Lesson

class Video(models.Model):
    PROVIDER_CHOICES = [
        ("local", "Local"),
        ("s3", "AWS S3"),
        ("vimeo", "Vimeo"),
        ("youtube", "YouTube"),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
    video_url = models.CharField(max_length=500, blank=True)  # URL finale
    uploaded_file = models.FileField(upload_to="videos/", blank=True, null=True)  # Upload local
    duration = models.PositiveIntegerField()  # secondes
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default="local")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lesson.title} - {self.id}"
