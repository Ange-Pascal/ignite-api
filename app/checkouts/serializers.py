# checkouts/serializers.py
from rest_framework import serializers
from .models import Checkout
from carts.models import Cart

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ["id", "user", "cart", "total_amount", "payment_method", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "total_amount", "status", "created_at", "updated_at"]

    def validate_cart(self, value):
        if value.status != "active":
            raise serializers.ValidationError("Cart has already been checked out or abandoned.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        cart = validated_data["cart"]

        # Calculer le total du panier
        total_amount = sum(item.price * item.quantity for item in cart.items.all())

        checkout = Checkout.objects.create(
            user=user,
            cart=cart,
            total_amount=total_amount,
            payment_method=validated_data["payment_method"],
            status="pending"
        )

        # Marquer le panier comme checked_out
        cart.status = "checked_out"
        cart.save()

        return checkout
