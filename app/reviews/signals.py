from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F, Avg
from .models import Review

@receiver(post_save, sender=Review)
def update_course_stats_on_save(sender, instance, created, **kwargs):
    """
    Met à jour le nombre total d'avis et la note moyenne lors de l'ajout d'une review.
    """
    course = instance.course

    if created:
        # 1. On incrémente le compteur total_reviews
        course.__class__.objects.filter(pk=course.pk).update(
            total_reviews=F('total_reviews') + 1
        )

    # 2. On recalcule la moyenne (rating)
    # aggregate renvoie un dictionnaire : {'rating__avg': 4.5}
    stats = Review.objects.filter(course=course).aggregate(Avg('rating'))
    new_average = stats['rating__avg'] or 0

    # 3. Mise à jour du champ FloatField
    course.average_rating = round(new_average, 2)
    course.save()

@receiver(post_delete, sender=Review)
def update_course_stats_on_delete(sender, instance, **kwargs):
    """
    Met à jour les stats lors de la suppression d'une review.
    """
    course = instance.course

    # 1. On décrémente le compteur
    course.__class__.objects.filter(
        pk=course.pk,
        total_reviews__gt=0
    ).update(
        total_reviews=F('total_reviews') - 1
    )

    # 2. On recalcule la moyenne
    stats = Review.objects.filter(course=course).aggregate(Avg('rating'))
    new_average = stats['rating__avg'] or 0

    course.average_rating = round(new_average, 2)
    course.save()


