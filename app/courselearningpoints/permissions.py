from rest_framework import permissions

class IsInstructorOwnerOrAdmin(permissions.BasePermission):
    """
    Permission pour Ignite :
    - Lecture : Tout le monde (SAFE_METHODS).
    - Modification : Admin (présent dans user.roles) OU Propriétaire (Instructor).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # 1. Vérification du rôle Admin dans le ManyToMany
        # .exists() est plus performant que de charger toute la liste
        if request.user.roles.filter(name__iexact="admin").exists():
            return True

        # 2. Vérification de la propriété (Propriétaire)
        # Si l'objet est le cours lui-même
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user

        # Si l'objet est lié à un cours (LearningPoint, Requirement)
        if hasattr(obj, 'course'):
            return obj.course.instructor == request.user

        return False
