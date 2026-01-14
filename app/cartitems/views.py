# cartitems/views.py
from rest_framework import viewsets, permissions
from .models import CartItem
from .serializers import CartItemSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    """
    Gestion des CartItems pour l'utilisateur connecté
    - List: liste tous les items du cart actif
    - Create: ajoute un item au cart actif
    - Retrieve, Update, Destroy: uniquement sur les items de l'utilisateur
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()  # Nécessaire pour drf-spectacular

    def get_queryset(self):
        """
        On ne retourne que les CartItems de l'utilisateur
        et uniquement dans le cart actif
        """
        user = self.request.user
        return CartItem.objects.filter(cart__user=user, cart__status='active')

    def perform_create(self, serializer):
        """
        Assignation automatique du CartItem à l'utilisateur et cart actif
        """
        # Si tu veux forcer le cart actif automatiquement :
        active_cart = self.request.user.carts.filter(status='active').first()
        serializer.save(cart=active_cart)
