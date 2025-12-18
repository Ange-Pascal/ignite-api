from rest_framework import serializers
from django.utils.text import slugify
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["slug"]

    def create(self, validated_data):
        title = validated_data.get("title")
        base_slug = slugify(title)
        slug = base_slug
        counter = 1

        while Course.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        validated_data["slug"] = slug
        return super().create(validated_data)
