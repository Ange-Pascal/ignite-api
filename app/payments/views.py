# payments/views.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 🔐 L’utilisateur ne voit que SES paiements
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 🔒 sécurité supplémentaire (défense en profondeur)
        serializer.save(user=self.request.user)
