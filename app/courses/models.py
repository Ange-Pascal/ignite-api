from django.db import models
from users.models import User
from categories.models import Category
from subcategories.models import SubCategory

class Course(models.Model):

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("all", "All"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    LANGUAGE_CHOICES = [
        ("english", "English"),
        ("French", "french"),
    ]
    user = models.ForeignKey(
        User,
        related_name="courses",
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        related_name="courses",
        on_delete=models.CASCADE
    )
    sub_category = models.ForeignKey(
        SubCategory,
        related_name="courses",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    #GET
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thumbnail = models.CharField(max_length=255)
    promo_video_url = models.CharField(max_length=255)
    # Fais automatiquement dans le signal review
    average_rating = models.FloatField(default=0)
    # Fais automatiquement dans le signal inscription
    total_students = models.IntegerField(default=0)

     # Fais automatiquement dans le signal review
    total_reviews = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
