from django.db import models

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ex: "Card", "PayPal"
    code = models.CharField(max_length=50, unique=True)   # ex: "card", "paypal"
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
