# checkouts/models.py
from django.db import models
from users.models import User
from carts.models import Cart

class Checkout(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("card", "Card"),
        ("paypal", "Paypal"),
        ("cash", "Cash"),
    )

    user = models.ForeignKey(User, related_name="checkouts", on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, related_name="checkout", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checkout #{self.id} - {self.user.email} - {self.status}"
