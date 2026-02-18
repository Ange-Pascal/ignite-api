from rest_framework import permissions

class IsAdminOrCourseOwner(permissions.BasePermission):
    """
    Permission pour permettre uniquement aux admins ou au créateur du cours
    de modifier ou supprimer les objets liés (Requirements, Lessons, etc.).
    """

    def has_permission(self, request, view):
        # Tout le monde peut voir (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Pour créer, il faut au moins être connecté
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS sont autorisées pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # On vérifie si l'utilisateur a le rôle admin
        is_admin = request.user.roles.filter(name="admin").exists()

        # On vérifie si l'utilisateur est le propriétaire du cours
        # Note : obj ici est CourseRequirement, donc on accède à obj.course.user
        is_owner = obj.course.user == request.user

        return is_admin or is_owner
