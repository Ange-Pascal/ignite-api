from django.test import TestCase
from subcategories.models import Category, SubCategory


class SubCategoryModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Développement",
            slug="developpement"
        )

    def test_create_subcategory_successful(self):
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Backend",
            slug="backend"
        )

        self.assertEqual(subcategory.name, "Backend")
        self.assertEqual(subcategory.category, self.category)

    def test_subcategory_str(self):
        subcategory = SubCategory.objects.create(
            category=self.category,
            name="Frontend",
            slug="frontend"
        )

        self.assertEqual(str(subcategory), subcategory.name)

    def test_subcategory_slug_unique_per_category(self):
        SubCategory.objects.create(
            category=self.category,
            name="Mobile",
            slug="mobile"
        )

        with self.assertRaises(Exception):
            SubCategory.objects.create(
                category=self.category,
                name="Mobile Dev",
                slug="mobile"
            )
