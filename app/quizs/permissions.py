from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

class IsAdminOrInstructorOwner(BasePermission):
    """
    Permission personnalisée :
    - Admin : accès total (is_staff=True ou rôle 'admin')
    - Instructor : accès seulement à ses propres objets
    - Student / autres : aucun accès pour create, update, delete, retrieve
    - Lecture (list/retrieve) :
        - Admin : tous
        - Instructor : seulement les siens
        - Student : aucun
    """

    def has_permission(self, request, view):
        """
        Vérifie si l'utilisateur a accès à la vue (list, create, etc.)
        """
        if not request.user or not request.user.is_authenticated:
            return False

        # Tous les utilisateurs authentifiés peuvent accéder à list ou retrieve
        if view.action in ["list", "retrieve"]:
            return True

        # Create / Update / Delete : seuls admin et instructors peuvent
        user_roles = list(request.user.roles.values_list("name", flat=True))
        if view.action in ["create", "update", "partial_update", "destroy"]:
            if request.user.is_staff or "admin" in user_roles or "instructor" in user_roles:
                return True
            # sinon blocage
            return False

        return True  # fallback

    def has_object_permission(self, request, view, obj):
        """
        Vérifie l'accès à un objet spécifique (retrieve, update, delete)
        """
        user_roles = list(request.user.roles.values_list("name", flat=True))

        # 🔹 Admin full access
        if request.user.is_staff or "admin" in user_roles:
            return True

        # 🔹 Instructor : uniquement propriétaire
        if "instructor" in user_roles:
            if obj.created_by == request.user:
                return True
            else:
                # Bloque l'accès pour tout objet non possédé
                raise PermissionDenied("Vous n'avez pas accès à ce quiz.")

        # 🔹 Student / autres : aucun accès aux objets
        if view.action in ["retrieve", "update", "partial_update", "destroy"]:
            raise PermissionDenied("Vous n'avez pas accès à ce quiz.")

        return False
