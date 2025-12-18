# cartitems/views.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer

class CartItemViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user, cart__status='active')
