from rest_framework.permissions import BasePermission, SAFE_METHODS


class CoursePermission(BasePermission):

    def has_permission(self, request, view):
        # 🔓 Lecture publique
        if request.method in SAFE_METHODS:
            return True

        # 🔐 Écriture → utilisateur authentifié requis
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # 🔓 Lecture publique
        if request.method in SAFE_METHODS:
            return True

        # 🔐 Sécurité
        if not request.user or not request.user.is_authenticated:
            return False

        # 👑 Admin
        if request.user.roles.filter(name="admin").exists():
            return True

        # 👨‍🏫 Instructor propriétaire
        if request.user.roles.filter(name="instructor").exists():
            return obj.user == request.user

        return False
