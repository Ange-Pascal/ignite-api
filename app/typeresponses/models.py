from django.db import models

class TypeResponse(models.Model):
    """
    Répresente le type de reponse
    par exemple : reponse à uploader le fichier
    """

    name= models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type de Response"
        verbose_name_plural = "Types de Response"
        ordering = ['name']

    def __str__(self):
        return self.name
