from rest_framework import serializers
from subcategories.models import SubCategory
from categories.models import Category



class SubCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model = SubCategory
        fields = ["id", "category_id", "name", "slug"]
