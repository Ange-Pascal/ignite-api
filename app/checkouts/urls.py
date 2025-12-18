# checkouts/urls.py
from rest_framework.routers import DefaultRouter
from .views import CheckoutViewSet

router = DefaultRouter()
router.register(r"checkouts", CheckoutViewSet, basename="checkout")

urlpatterns = router.urls
