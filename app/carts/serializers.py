# carts/serializers.py
from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'total_amount', 'currency', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user

        # Vérifie si l'utilisateur a déjà un cart actif
        if Cart.objects.filter(user=user, status='active').exists():
            raise serializers.ValidationError("You already have an active cart.")

        cart = Cart.objects.create(user=user, **validated_data)
        return cart

    def update(self, instance, validated_data):
        # Interdire la modification du user
        validated_data.pop('user', None)
        return super().update(instance, validated_data)
