from rest_framework.viewsets import ModelViewSet
from subcategories.models import SubCategory

from subcategories.serializers import SubCategorySerializer
from subcategories.permissions import IsAdminUserOrReadOnly



class SubCategoryViewSet(ModelViewSet):
    queryset = SubCategory.objects.select_related("category")
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
