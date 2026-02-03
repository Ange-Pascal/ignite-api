from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from roles.models import Role
from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APIClient


User = get_user_model()

class JWTAuthTests(APITestCase):


    def setUp(self):
        self.password = "test123"

        self.student_role = Role.objects.create(
            name="student",
            description= "Default role"
        )
        self.admin_role = Role.objects.create(
            name="admin",
            description="Role de l'admin"
        )

        self.student = User.objects.create_user(
            email= "student@test.com",
            password = self.password,
            is_active = True
        )

        self.student.roles.add(self.student_role)


        self.admin = User.objects.create_user(
            email="admin@test.com",
            password= self.password,
            is_active = True
        )

        self.admin.roles.add(self.admin_role)


    def test_student_has_role_student(self):
        self.assertTrue(
            self.student.roles.filter(name="student").exists()
        )

    def test_admin_has_role_admin(self):
        self.assertTrue(
            self.admin.roles.filter(name="admin").exists()
        )


    def test_login_wrong_password_return_401(self):
        response = self.client.post("/api/token/", {
            "email": "student@test.com",
            "password": "wrong"
        })
        self.assertTrue(response.status_code, 401)

    def test_inactive_user_cannot_get_token(self):
        self.student.is_active = False
        self.student.save()


        response = self.client.post("/api/token/", {
            "email": self.student.email,
            "password": self.password
        })

        self.assertTrue(response.status_code, 401)


    def test_valid_returns_new_access(self):
        response = self.client.post("/api/token/", {
            "email": self.student.email,
            "password": self.password
        }, format="json")

        refresh = response.data["refresh"]

        response = self.client.post("/api/token/refresh/", {
            "refresh" : refresh
        }, format="json")


        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_invalid_refresh_returns_401(self):
        response = self.client.post("/api/token/refresh/", {
            "refresh": "invalid.token.value"
        })

        self.assertTrue(response.status_code, 401)

    def test_protected_view_without_token(self):
        url = reverse("user:protected-view")
        client = APIClient()
        response = self.client.get(url)  # pas self.get()
        self.assertEqual(response.status_code, 401)

    def test_admin_view_with_student_token(self):

        student_token = str(RefreshToken.for_user(self.student).access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {student_token}")
        url = reverse("user:admin-only")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_admin_view_with_admin_token(self):
        # Générer un token JWT pour l'admin
        admin_token = str(RefreshToken.for_user(self.admin).access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
        url = reverse("user:admin-only")
        response = self.client.get(url)  # ✅ utiliser get()

        self.assertEqual(response.status_code, 200)

