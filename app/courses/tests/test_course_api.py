from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from roles.models import Role
from categories.models import Category
from subcategories.models import SubCategory
from courses.models import Course
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class CourseAPITests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            "admin@example.com",
            "admin123"
        )

        self.instructor = User.objects.create_user(
            "instr@example.com",
            "instr123"
        )
        instructor_role, _ = Role.objects.get_or_create(name="instructor")
        self.instructor.roles.add(instructor_role)

        self.category = Category.objects.create(
            name="Développement",
            slug="developpement"
        )
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Backend",
            slug="backend"
        )

        self.course = Course.objects.create(
            user=self.instructor,
            category=self.category,
            sub_category=self.subcategory,
            title="Python avancé",
            slug="python-avance",
            subtitle="Maîtrisez Python",
            description="Formation complète",
            language="FR",
            level="advanced",
            price=100,
            discount_price=80,
            thumbnail="thumb.png",
            promo_video_url="video",
            requirements="Bases Python",
            what_you_will_learn="Python avancé",
            status="draft"
        )

    def test_retrieve_course_by_slug(self):
        url = reverse("course-detail", args=[self.course.slug])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["slug"], "python-avance")
