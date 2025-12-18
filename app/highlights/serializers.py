from rest_framework import serializers
from highlights.models import Highlight

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = ["id", "course", "label", "type"]
