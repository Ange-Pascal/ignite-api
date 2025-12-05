from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """Seul le propriétaire ou le superuser peut modifier/supprimer"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user
