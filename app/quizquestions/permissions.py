from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrInstructorQuizQuestionOwner(BasePermission):
    """
    Permissions pour QuizQuestion

    Règles :
    - Admin (is_staff ou rôle 'admin') : accès total
    - Instructor : CRUD uniquement sur les questions
      appartenant à ses propres quiz
    - Autres rôles : aucun accès
    """

    def has_permission(self, request, view):
        """
        Permission globale (list, create)
        """
        user = request.user

        if not user or not user.is_authenticated:
            return False

        user_roles = list(user.roles.values_list("name", flat=True))

        # Admin ou Instructor peuvent accéder au endpoint
        if user.is_staff or "admin" in user_roles or "instructor" in user_roles:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Permission par objet (retrieve, update, delete)
        """
        user = request.user
        user_roles = list(user.roles.values_list("name", flat=True))

        # 🔹 Admin : accès total
        if user.is_staff or "admin" in user_roles:
            return True

        # 🔹 Instructor : seulement si propriétaire du quiz parent
        if "instructor" in user_roles:
            return obj.quiz.created_by == user

        return False
