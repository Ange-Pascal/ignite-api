from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from categories.models import Category
from rest_framework_simplejwt.tokens import RefreshToken


CATEGORY_URL = reverse("category-list")


def create_user(email, password, is_admin=False):
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        is_staff=is_admin,
        is_superuser=is_admin
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
    }


class CategoryAPITests(APITestCase):

    def setUp(self):
        self.admin_user = create_user(
            "admin@example.com",
            "adminpass123",
            is_admin=True
        )
        self.normal_user = create_user(
            "user@example.com",
            "userpass123"
        )

    def test_list_categories(self):
        Category.objects.create(name="Design", slug="design")
        Category.objects.create(name="Web", slug="web")

        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_admin_can_create_category(self):
        token = get_tokens_for_user(self.admin_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token['access']}"
        )

        payload = {
            "name": "Backend",
            "slug": "backend"
        }

        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(slug="backend").exists())

    def test_non_admin_cannot_create_category(self):
        token = get_tokens_for_user(self.normal_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token['access']}"
        )

        payload = {
            "name": "DevOps",
            "slug": "devops"
        }

        res = self.client.post(CATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
