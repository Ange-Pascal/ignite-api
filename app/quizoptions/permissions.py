from rest_framework.permissions import BasePermission


class IsAdminOrInstructorOwner(BasePermission):
    """
    Permission pour QuizOption
    - Admin : accès total
    - Instructor : uniquement sur ses quiz
    - Autres : refus
    """

    def has_permission(self, request, view):
        user = request.user

        # 🔹 IMPORTANT : Swagger / schema safety
        if not user or not user.is_authenticated:
            return False

        # 🔹 Admin Django
        if user.is_staff:
            return True

        # 🔹 Sécurité : vérifier l'existence de roles
        if not hasattr(user, "roles"):
            return False

        # 🔹 Admin ou Instructor
        return user.roles.filter(
            name__in=["admin", "instructor"]
        ).exists()

    def has_object_permission(self, request, view, obj):
        user = request.user

        # 🔹 Swagger / sécurité
        if not user or not user.is_authenticated:
            return False

        # 🔹 Admin
        if user.is_staff:
            return True

        if not hasattr(user, "roles"):
            return False

        # 🔹 Admin via roles
        if user.roles.filter(name="admin").exists():
            return True

        # 🔹 Instructor propriétaire
        if user.roles.filter(name="instructor").exists():
            return obj.quiz_question.quiz.created_by == user

        return False
