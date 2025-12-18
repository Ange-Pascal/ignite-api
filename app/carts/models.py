from django.db import models
from users.models import User


class Cart(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("checked_out", "Checked out"),
        ("abandoned", "Abandoned"),
    )

    user = models.ForeignKey(
        User,
        related_name="carts",
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    # Snapshot du montant AU MOMENT DU PAIEMENT
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"Cart #{self.id} - {self.user.email} - {self.status}"

    def calculate_total(self):
        return sum(
            item.course.price * item.quantity
            for item in self.items.all()
        )

    def update_total(self):
        total = self.items.aggregate(total=models.Sum('price'))['total'] or 0
        self.total_amount = total
        self.save()

