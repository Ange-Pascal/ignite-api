from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.permissions import CoursePermission


class VideoPermission(BasePermission):
    """
    Les droits Video héritent des droits du Course
    """

    def has_permission(self, request, view):
        # même règle globale que Course
        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, video):
        course = video.lesson.module.course
        course_permission = CoursePermission()

        # Délégation directe 🔁
        return course_permission.has_object_permission(
            request, view, course
        )
