# checkouts/views.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Checkout
from .serializers import CheckoutSerializer

class CheckoutViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # L'utilisateur ne peut voir que ses propres checkouts
        return Checkout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = serializer.validated_data.get("cart")

        # Vérifier que le panier appartient bien à l'utilisateur
        if cart.user != self.request.user:
            raise PermissionDenied("You cannot checkout another user's cart.")

        # Sauvegarder le checkout avec le montant et le status
        serializer.save(
            user=self.request.user,
            total_amount=cart.total_amount,
            status="pending"
        )
