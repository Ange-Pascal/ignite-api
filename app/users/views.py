from rest_framework import generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
import os


from users.models import User
from roles.models import Role
from .serializers import UserSerializer, AuthTokenSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdminRole

ENV = os.environ.get("ENV", "local")


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "phone": user.phone,
                    "roles": [role.name for role in user.roles.all()],
                }
            },
            status=status.HTTP_201_CREATED
        )
        if ENV == "local":
            secure_cookie = False
        else:
            secure_cookie = True

        response.set_cookie(
            key="access",
            value=str(refresh.access_token),
            httponly=True,
            secure=secure_cookie,
            samesite="Lax"
        )
        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=secure_cookie,
            samesite="Lax"
        )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ManageUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListOrSelfView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        UserModel = get_user_model()
        if user.is_superuser:
            return UserModel.objects.all()
        return UserModel.objects.filter(id=user.id)

class UserDeleteView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"
    lookup_url_kwarg = "id"

class AddInstructorRoleView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            instructor_role = Role.objects.get(name="instructor")
        except Role.DoesNotExist:
            return Response({"error": "Instructor role not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if user.roles.filter(name="instructor").exists():
            return Response({"message": "This user is already an instructor."}, status=status.HTTP_200_OK)

        user.roles.add(instructor_role)

        return Response(
            {
                "message": "Instructor role added successfully.",
                "user_id": user.id,
                "roles": [role.name for role in user.roles.all()],
            },
            status=status.HTTP_200_OK
        )


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"Message": "JWT is correct"})


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]


    def get(self, request):
        return Response({"Message": "Admin autorized"})
