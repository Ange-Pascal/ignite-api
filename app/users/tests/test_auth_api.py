from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class AuthApiTests(APITestCase):

    def setUp(self):
        self.login_url = reverse("user:token_obtain_pair")
        self.user = User.objects.create_user(
            email="test@example.com",
            password="pass1234",
            name="Test Name"
        )

    def test_login_returns_jwt_tokens(self):
        """Le login doit retourner un acces et refresh token """
        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "pass1234"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials_fails(self):
        """Un mauvais password doit retourner 401"""
        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "wrong pass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

