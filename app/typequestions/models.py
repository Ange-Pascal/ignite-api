from django.db import models

class TypeQuestion(models.Model):
    """
    Répresente le type de question
    par exemple : question à choix multiple
    """

    name= models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type de Question"
        verbose_name_plural = "Types de Question"
        ordering = ['name']

    def __str__(self):
        return self.name