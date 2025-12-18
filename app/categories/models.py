from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
