# base.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from courses.models import Course
from lessons.models import Lesson
from modules.models import Module  # <- on importe Module
from categories.models import Category
from subcategories.models import  SubCategory
from roles.models import Role

User = get_user_model()

class BaseVideoTest(APITestCase):

    def create_user(self, role_name):
        import uuid

        unique_id = uuid.uuid4().hex[:6]
        email = f"{role_name}_{unique_id}@test.com"

        user = User.objects.create_user(
            email=email,
            password="password123"
        )

        # 🔑 récupérer ou créer le rôle
        role, _ = Role.objects.get_or_create(name=role_name)

        # 🔑 attacher le rôle au user
        user.roles.add(role)

        return user

    def create_course(self, instructor):
        category = Category.objects.create(name="Test Category")
        sub_category = SubCategory.objects.create(
            name="Test SubCategory",
            category=category
        )
        return Course.objects.create(
            title="Test Course",
            user=instructor,      # ou instructor si ton champ s'appelle 'user'
            category=category,
            sub_category=sub_category,
            subtitle="Test Subtitle",
            description="Test Description",
            language="English",
            level="beginner",
            price=100,
            discount_price=0,
            thumbnail="thumb.jpg",
            promo_video_url="promo.mp4",
            requirements="Requirements",
            what_you_will_learn="Learning outcomes",
            status="draft"
        )


    def create_module(self, course, title="Module 1", position=1):
        return Module.objects.create(
            title=title,
            course=course,
            position=position
        )

    def create_lesson(self, module, title="Lesson 1", position=1):
        """
        Maintenant la leçon prend un module et non plus un course
        """
        return Lesson.objects.create(
            module=module,
            title=title,
            position=position
        )
