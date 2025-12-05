from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")
USER_LIST_URL = reverse("user:list_or_self")


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            "email": "test@example.com",
            "password": "pass123",
            "name": "Test Name"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)



    def test_user_exits(self):
        payload = {"email": "test@example.com", "password": "pass123"}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)


        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




class UserMeAndListApiTests(APITestCase):
    """Tests profil et liste des utilisateurs avec rôles"""

    def setUp(self):
        # Créer les utilisateurs avec rôles
        self.admin = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            name="Admin"
        )
        self.user1 = get_user_model().objects.create_user(
            email="user1@example.com",
            password="pass123",
            name="User One"
        )
        self.user2 = get_user_model().objects.create_user(
            email="user2@example.com",
            password="pass123",
            name="User Two"
        )

    def _get_jwt_token(self, user):
        """Helper pour générer un JWT token pour un user"""
        res = self.client.post(TOKEN_URL, {
            "email": user.email,
            "password": "admin123" if user.is_superuser else "pass123"
        })
        return res.data["access"]

    def test_retrieve_profile(self):
        """L'utilisateur connecté récupère son profil"""
        token = self._get_jwt_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user1.email)
        self.assertEqual(res.data["name"], self.user1.name)

    def test_admin_sees_all_users(self):
        """Un admin doit voir tous les utilisateurs"""
        token = self._get_jwt_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        emails = [u["email"] for u in res.data]
        self.assertIn("admin@example.com", emails)
        self.assertIn("user1@example.com", emails)
        self.assertIn("user2@example.com", emails)

    def test_user_sees_only_self(self):
        """Un utilisateur normal ne voit que son propre profil dans la liste"""
        token = self._get_jwt_token(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["email"], self.user2.email)
        self.assertEqual(res.data[0]["name"], self.user2.name)

    def test_unauthenticated_user_cannot_access_list(self):
        """Un utilisateur non authentifié ne peut pas accéder à la liste"""
        res = self.client.get(USER_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminUserDeleteTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.superuser = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="admin123"
        )
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="user123"
        )

        # Authentification du superuser
        self.client.force_authenticate(user=self.superuser)

    def test_superuser_can_delete_user(self):
        url = reverse("user:user_delete", args=[self.user.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(get_user_model().objects.filter(id=self.user.id).exists())

    def test_non_superuser_cannot_delete_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user:user_delete", args=[self.user.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
