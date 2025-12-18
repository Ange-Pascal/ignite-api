# cartitems/serializers.py
from rest_framework import serializers
from .models import CartItem
from carts.models import Cart

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'course', 'quantity', 'price', 'added_at']
        read_only_fields = ['cart', 'price', 'added_at']

    def validate(self, attrs):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user, status='active')
        course = attrs['course']

        if CartItem.objects.filter(cart=cart, course=course).exists():
            raise serializers.ValidationError("Course already in cart.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user, status='active')
        cart_item = CartItem.objects.create(
            cart=cart,
            course=validated_data['course'],
            quantity=validated_data.get('quantity', 1),
            price=validated_data['course'].price
        )
        # Mettre à jour le total du panier après ajout
        cart.total_amount = sum(item.price * item.quantity for item in cart.items.all())
        cart.save()
        return cart_item
