# payments/models.py
from django.db import models
from users.models import User
from checkouts.models import Checkout
from paymentmethods.models import PaymentMethod


class Payment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    checkout = models.ForeignKey(
        Checkout,
        related_name="payments",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        related_name="payments",
        on_delete=models.CASCADE
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        related_name="payments",
        on_delete=models.PROTECT  # très important (on ne supprime pas une méthode utilisée)
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="USD"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    failure_reason = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency} - {self.status}"
