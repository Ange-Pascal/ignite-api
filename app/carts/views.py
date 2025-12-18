# carts/views.py
from rest_framework import viewsets, permissions
from .models import Cart
from .serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit que ses propres carts
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assignation automatique de l'utilisateur connecté
        serializer.save()
