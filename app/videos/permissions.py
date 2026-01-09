from rest_framework.permissions import BasePermission, SAFE_METHODS
from courses.permissions import CoursePermission


class VideoPermission(BasePermission):
    """
    Les droits Video héritent des droits du Course
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            lesson_id = request.data.get("lesson")
            if not lesson_id:
                return False

            from lessons.models import Lesson
            try:
                lesson = Lesson.objects.get(id=lesson_id)
            except Lesson.DoesNotExist:
                return False

            if request.user.roles.filter(name="admin").exists():
                return True

            if request.user.roles.filter(name="instructor").exists():
                return lesson.module.course.user == request.user

            return False

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin : tout
        if user.roles.filter(name="admin").exists():
            return True

        # Instructor : seulement ses vidéos
        if user.roles.filter(name="instructor").exists():
            return obj.lesson.module.course.user == user

        return False

