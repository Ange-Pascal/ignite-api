from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from users.models import User
from roles.models import Role



from .serializers import UserSerializer, AuthTokenSerializer, CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user



class UserListOrSelfView(generics.ListAPIView):
    """
    -Admin : voir tous les users
    -User Normal : voir seulement lui-même
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        User = get_user_model()

        if user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)


class UserDeleteView(generics.DestroyAPIView):
    """
    Supprimer un utilisateur par son ID.
    Seul le superuser peut effectuer cette action.
    """
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAdminUser]  # seulement superuser

    lookup_field = "id"            # champ utilisé dans la DB
    lookup_url_kwarg = "id"        # paramètre envoyé dans l’URL


class AddInstructorRoleView(APIView):
    permission_classes = [IsAdminUser]  # 🔐 Seul admin peut promouvoir

    def post(self, request, user_id):
        """Ajoute le rôle 'instructor' à un user."""

        # Vérifier que l'utilisateur existe
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer le rôle instructeur
        try:
            instructor_role = Role.objects.get(name="instructor")
        except Role.DoesNotExist:
            return Response({"error": "Instructor role not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Empêcher les doublons
        if user.roles.filter(name="instructor").exists():
            return Response({"message": "This user is already an instructor."}, status=status.HTTP_200_OK)

        # Ajouter le rôle
        user.roles.add(instructor_role)

        return Response(
            {
                "message": "Instructor role added successfully.",
                "user_id": user.id,
                "roles": [role.name for role in user.roles.all()],
            },
            status=status.HTTP_200_OK
        )
