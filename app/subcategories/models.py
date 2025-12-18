from django.db import models
from categories.models import Category


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField()

    class Meta:
        unique_together = ("category", "slug")
        ordering = ["name"]

    def __str__(self):
        return self.name
