from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from categories.models import Category
from categories.serializers import CategorySerializer
from categories.permissions import IsAdminUserOrReadOnly


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
