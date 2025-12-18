# reviews/tests/test_review_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from roles.models import Role
from categories.models import Category
from subcategories.models import SubCategory
from courses.models import Course
from reviews.models import Review
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class ReviewPermissionTests(APITestCase):

    def setUp(self):
        # Roles
        self.student_role = Role.objects.create(name="student")
        self.instructor_role = Role.objects.create(name="instructor")

        # Users
        self.student = User.objects.create_user(email="student@test.com", password="password123")
        self.student.roles.add(self.student_role)

        self.instructor = User.objects.create_user(email="instructor@test.com", password="password123")
        self.instructor.roles.add(self.instructor_role)

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

        self.url = reverse("review-list")

    def test_student_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.student)}")
        data = {
            "course": self.course.id,
            "user": self.student.id,
            "rating": 5,
            "comment": "Excellent course!"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_instructor_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.instructor)}")
        data = {
            "course": self.course.id,
            "user": self.instructor.id,
            "rating": 4,
            "comment": "Good content"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_cannot_create_review(self):
        data = {
            "course": self.course.id,
            "user": 999,
            "rating": 3,
            "comment": "Should fail"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Review.objects.count(), 0)
