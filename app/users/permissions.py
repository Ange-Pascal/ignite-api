from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):

        user = request.user

        if not user or not user.is_authenticated:
            return False


        return user.roles.filter(name="admin").exists()



class IsStudendtRole(BasePermission):
    def has_permission(self, request, view):

        return request.user.roles.filter(name="student").exists()
