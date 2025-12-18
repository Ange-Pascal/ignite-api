from rest_framework.routers import DefaultRouter
from categories.views import CategoryViewSet
from subcategories.views import SubCategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("subcategories", SubCategoryViewSet, basename="subcategory")

urlpatterns = router.urls
