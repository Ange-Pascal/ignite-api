# outcomes/views.py
from rest_framework.viewsets import ModelViewSet
from outcomes.models import Outcome
from outcomes.serializers import OutcomeSerializer
from outcomes.permissions import IsAdminOrInstructor
from rest_framework.permissions import IsAuthenticated

class OutcomeViewSet(ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrInstructor]
