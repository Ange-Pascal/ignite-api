from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from subcategories.models import Category, SubCategory
from rest_framework_simplejwt.tokens import RefreshToken


SUBCATEGORY_URL = reverse("subcategory-list")


def create_user(email, password, is_admin=False):
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        is_staff=is_admin,
        is_superuser=is_admin
    )


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class SubCategoryAPITests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Design",
            slug="design"
        )

        self.admin = create_user(
            "admin@example.com",
            "admin123",
            is_admin=True
        )

        self.user = create_user(
            "user@example.com",
            "user123"
        )

    def test_list_subcategories(self):
        SubCategory.objects.create(
            category=self.category,
            name="UI",
            slug="ui"
        )

        res = self.client.get(SUBCATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_admin_can_create_subcategory(self):
        token = get_token(self.admin)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

        payload = {
            "category": self.category.id,
            "name": "UX",
            "slug": "ux"
        }

        res = self.client.post(SUBCATEGORY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SubCategory.objects.filter(slug="ux").exists())

    def test_admin_can_create_subcategory(self):
        token = get_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        payload = {
            "category_id": self.category.id,
            "name": "UX",
            "slug": "ux"
        }

        res = self.client.post(SUBCATEGORY_URL, payload, format='json')  # format='json' recommandé

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SubCategory.objects.filter(slug="ux").exists())
