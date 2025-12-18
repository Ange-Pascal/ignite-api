from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r'carts/items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls
