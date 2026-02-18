from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, CourseMetaDataView

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("meta-data/", CourseMetaDataView.as_view(), name="course-metadata"),
    path("", include(router.urls))
]


