from rest_framework.permissions import BasePermission

class IsAdminOrInstructor(BasePermission):
    message = "Seuls les administrateurs ou instructeurs peuvent créer un module."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.roles.filter(
            name__in=["admin", "instructor"]
        ).exists()
