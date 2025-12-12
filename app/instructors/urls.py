from rest_framework.routers import DefaultRouter
from .views import InstructorProfileView

# <- Très important si tu veux utiliser le namespace
app_name = "instructor"

router = DefaultRouter()
router.register(r'profiles', InstructorProfileView, basename='instructorprofile')

urlpatterns = router.urls
