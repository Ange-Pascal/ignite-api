from rest_framework.permissions import BasePermission, SAFE_METHODS


class TypeQuestionPermission(BasePermission):
    """
    Lecture publique, ecriture seul admin
    """

    def has_permission(self, request, view):
        # Lecture publique

        if request.method in SAFE_METHODS:
            return True

        # Ecriture user authentifié plus role admin
        user = request.user

        return (
            user and
            user.is_authenticated and
            user.roles.filter(name="admin").exists()
        )

