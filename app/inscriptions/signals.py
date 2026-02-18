from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Inscription # Import relatif (sécurisé)

@receiver(post_save, sender=Inscription)
def increment_students(sender, instance, created, **kwargs):
    """
    Incrémente le compteur du cours lorsqu'une inscription est créée.
    """
    if created:
        # On accède à la classe du modèle Course sans l'importer explicitement en haut
        # pour éviter les imports circulaires.
        instance.course.__class__.objects.filter(pk=instance.course.pk).update(
            total_students=F('total_students') + 1
        )

#Actuellement, si une inscription passe du statut "active" à "cancelled", elle reste en base de données donc ton compteur ne bouge pas

@receiver(post_delete, sender=Inscription)
def decrement_students(sender, instance, **kwargs):
    """
    Décrémente le compteur si une inscription est supprimée.
    """
    instance.course.__class__.objects.filter(
        pk=instance.course.pk,
        total_students__gt=0
    ).update(
        total_students=F('total_students') - 1
    )
