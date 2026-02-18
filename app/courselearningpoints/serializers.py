from rest_framework import serializers
from .models import CourseLearningPoint

class LearningPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLearningPoint
        fields = ['id', 'content']

