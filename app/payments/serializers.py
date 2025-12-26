from rest_framework import serializers
from django.db import transaction
from payments.models import Payment
from checkouts.models import Checkout
from paymentmethods.models import PaymentMethod
from inscriptions.models import Inscription


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "checkout",
            "user",
            "payment_method",
            "amount",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "amount",
            "status",
            "created_at",
        ]

    # 🔒 sécurité checkout
    def validate_checkout(self, checkout: Checkout):
        request = self.context["request"]

        if checkout.user != request.user:
            raise serializers.ValidationError(
                "Vous ne pouvez pas payer le checkout d’un autre utilisateur."
            )

        if checkout.status == "completed":
            raise serializers.ValidationError(
                "Ce checkout a déjà été payé."
            )

        return checkout

    # 🔒 méthode de paiement valide
    def validate_payment_method(self, payment_method: PaymentMethod):
        if not payment_method.is_active:
            raise serializers.ValidationError(
                "Cette méthode de paiement est désactivée."
            )
        return payment_method

    # 🚀 logique métier centrale
    @transaction.atomic
    def create(self, validated_data):
        checkout = validated_data["checkout"]

        # 🔒 backend contrôle tout
        validated_data["amount"] = checkout.total_amount
        validated_data["status"] = "completed"  # simulation paiement OK

        payment = Payment.objects.create(**validated_data)

        # ✅ checkout payé
        checkout.status = "completed"
        checkout.save(update_fields=["status"])

        # ✅ inscriptions automatiques
        cart = checkout.cart
        for item in cart.items.all():
            Inscription.objects.get_or_create(
                user=checkout.user,
                course=item.course,
                defaults={"status": "approved"},
            )

        return payment
