# instructors/urls.py
from rest_framework.routers import DefaultRouter
from .views import InstructorProfileView

app_name = "instructor"

router = DefaultRouter()
router.register(r'profiles', InstructorProfileView, basename='profile')

urlpatterns = router.urls
