# outcomes/serializers.py
from rest_framework import serializers
from outcomes.models import Outcome

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ["id", "course", "label"]
