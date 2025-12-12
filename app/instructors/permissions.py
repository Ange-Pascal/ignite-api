from rest_framework.permissions import BasePermission

class IsInstructorAndOwnerOrAdmin(BasePermission):
    """
    - L'utilisateur doit être instructeur pour créer un profil.
    - Un instructeur ne peut modifier que son propre profil.
    - Un admin peut tout faire.
    """

    def has_permission(self, request, view):
        # Admin peut tout faire
        if request.user.roles.filter(name="admin").exists():
            return True

        # Autoriser seulement les instructeurs à créer un profil
        if view.action == "create":
            return request.user.roles.filter(name="instructor").exists()

        return True

    def has_object_permission(self, request, view, obj):
        # Admin = accès total
        if request.user.roles.filter(name="admin").exists():
            return True

        # Instructor = accès seulement à son propre profil
        return obj.user == request.user
