from rest_framework.permissions import BasePermission

class IsStudentOrAdminForQuizAttempt(BasePermission):
    """
    Permission pour QuizAttempt :

    - Admin : peut créer n'importe quelle tentative
    - Student : peut créer uniquement sa propre tentative
    - Instructor / autres : aucun accès à la création
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Récupération des rôles
        user_roles = list(user.roles.values_list("name", flat=True))

        # 🔹 Admin : tout accès
        if user.is_staff or "admin" in user_roles:
            return True

        # 🔹 Student : accès POST uniquement
        if "student" in user_roles:
            return True

        # 🔹 Tous les autres : aucun accès
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        user_roles = list(user.roles.values_list("name", flat=True))

        # 🔹 Admin : accès total
        if user.is_staff or "admin" in user_roles:
            return True

        # 🔹 Student : seulement sa propre tentative
        if "student" in user_roles:
            return obj.user == user

        # 🔹 Tous les autres : aucun accès
        return False
