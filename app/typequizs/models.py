from django.db import models

class TypeQuiz(models.Model):
    """
    Répresente le type pedagogique d'un quiz
    par exemple : diagnostic, formatif, sommative, certificatif.
    """

    name= models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type de Quiz"
        verbose_name_plural = "Types de Quiz"
        ordering = ['name']

    def __str__(self):
        return self.name