from django.test import TestCase
from categories.models import Category


class CategoryModelTests(TestCase):

    def test_create_category_successful(self):
        category = Category.objects.create(
            name="web development",
            slug="web-development"
        )

        self.assertEqual(category.name, "web development")
        self.assertEqual(category.slug, "web-development")
        self.assertIsNotNone(category.id)

    def test_category_str(self):
        category = Category.objects.create(
            name="design",
            slug="design"
        )
        self.assertEqual(str(category), category.name)

    def test_category_slug_unique(self):
        Category.objects.create(
            name="marketing",
            slug="marketing"
        )

        with self.assertRaises(Exception):
            Category.objects.create(
                name="marketing Digital",
                slug="marketing"
            )

