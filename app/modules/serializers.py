# modules/serializers.py
from rest_framework import serializers
from modules.models import Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            "id",
            "course",
            "title",
            "description",
            "position",
        ]
