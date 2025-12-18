# cartitems/models.py
from django.db import models
from carts.models import Cart
from courses.models import Course

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        related_name="cart_items",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'course')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.course.title} in Cart #{self.cart.id}"

    def save(self, *args, **kwargs):
        # Mettre à jour le prix actuel du cours au moment de l'ajout
        if not self.price:
            self.price = self.course.price
        super().save(*args, **kwargs)
        # Recalculer le total du panier
        self.cart.update_total()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Recalculer le total du panier après suppression
        self.cart.update_total()
