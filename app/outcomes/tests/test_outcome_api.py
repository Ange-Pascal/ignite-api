# outcomes/tests/test_outcome_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from roles.models import Role
from categories.models import Category
from subcategories.models import SubCategory
from courses.models import Course
from outcomes.models import Outcome
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class OutcomePermissionTests(APITestCase):

    def setUp(self):
        # Roles
        self.admin_role = Role.objects.create(name="admin")
        self.instructor_role = Role.objects.create(name="instructor")
        self.student_role = Role.objects.create(name="student")

        # Users
        self.admin = User.objects.create_user(email="admin@test.com", password="password123")
        self.admin.roles.add(self.admin_role)

        self.instructor = User.objects.create_user(email="instructor@test.com", password="password123")
        self.instructor.roles.add(self.instructor_role)

        self.student = User.objects.create_user(email="student@test.com", password="password123")
        self.student.roles.add(self.student_role)

        # Category / SubCategory
        self.category = Category.objects.create(name="Programming")
        self.sub_category = SubCategory.objects.create(name="Web Development", category=self.category)

        # Course
        self.course = Course.objects.create(
            user=self.instructor,
            category=self.category,
            sub_category=self.sub_category,
            title="Django REST API",
            slug="django-rest-api",
            subtitle="Learn DRF from scratch",
            description="Complete course on Django REST Framework",
            language="English",
            level="beginner",
            price=100.00,
            discount_price=50.00,
            thumbnail="thumbnail.jpg",
            promo_video_url="https://youtu.be/example",
            requirements="Basic Python knowledge",
            what_you_will_learn="Build REST APIs with Django",
            status="published",
        )

        self.url = reverse("outcome-list")

    def test_admin_can_create_outcome(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.admin)}")
        data = {"course": self.course.id, "label": "Admin Outcome"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Outcome.objects.count(), 1)

    def test_instructor_can_create_outcome(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.instructor)}")
        data = {"course": self.course.id, "label": "Instructor Outcome"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_outcome(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.student)}")
        data = {"course": self.course.id, "label": "Forbidden Outcome"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Outcome.objects.count(), 0)
