# lessons/tests/test_lesson_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from roles.models import Role
from categories.models import Category
from subcategories.models import SubCategory
from courses.models import Course
from modules.models import Module
from lessons.models import Lesson
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class LessonPermissionTests(APITestCase):

    def setUp(self):
        # Roles
        self.admin_role = Role.objects.create(name="admin")
        self.instructor_role = Role.objects.create(name="instructor")
        self.student_role = Role.objects.create(name="student")

        # Users
        self.admin = User.objects.create_user(
            email="admin@test.com", password="password123"
        )
        self.admin.roles.add(self.admin_role)

        self.instructor = User.objects.create_user(
            email="instructor@test.com", password="password123"
        )
        self.instructor.roles.add(self.instructor_role)

        self.student = User.objects.create_user(
            email="student@test.com", password="password123"
        )
        self.student.roles.add(self.student_role)

        # Category / SubCategory
        self.category = Category.objects.create(name="Programming")
        self.sub_category = SubCategory.objects.create(
            name="Web Development", category=self.category
        )

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

        # Module
        self.module = Module.objects.create(
            course=self.course,
            title="Module 1",
            description="First module",
            position=1
        )

        self.url = reverse("lesson-list")

    def test_admin_can_create_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.admin)}")
        data = {
            "module": self.module.id,
            "title": "Admin Lesson",
            "position": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_instructor_can_create_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.instructor)}")
        data = {
            "module": self.module.id,
            "title": "Instructor Lesson",
            "position": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.student)}")
        data = {
            "module": self.module.id,
            "title": "Forbidden Lesson",
            "position": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.count(), 0)
