from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseTypeQuizTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def create_user(self, role_name="student"):
        email = f"{role_name}@example.com"
        password = "testpass123"

        user = User.objects.create_user(
            email=email,
            password=password
        )

        # Ajout du rôle si ce n'est pas "student"
        if role_name != "student":
            role, _ = user.roles.model.objects.get_or_create(name=role_name)
            user.roles.add(role)

        return user
