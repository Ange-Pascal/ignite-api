from django.test import TestCase
from categories.models import Category
from subcategories.models import SubCategory

from users.models import User
from courses.models import Course


class CourseModelTests(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin123"
        )
        self.instructor = User.objects.create_user(
            email="instr@example.com",
            password="instr123"
        )
        # On ajoute rôle instructor à cet utilisateur
        instructor_role, _ = self.instructor.roles.get_or_create(name="instructor")
        self.instructor.roles.add(instructor_role)

        self.category = Category.objects.create(name="Développement", slug="dev")
        self.subcategory = SubCategory.objects.create(
            category=self.category,
            name="Backend",
            slug="backend"
        )

    def test_create_course_successful(self):
        course = Course.objects.create(
            user=self.instructor,
            category=self.category,
            sub_category=self.subcategory,
            title="Python avancé",
            slug="python-avance",
            subtitle="Devenez expert Python",
            description="Formation complète",
            language="FR",
            level="advanced",
            price=100,
            discount_price=80,
            thumbnail="thumbnail.png",
            promo_video_url="https://video.com/vid",
            requirements="Connaissances de base",
            what_you_will_learn="Programmation avancée",
            status="draft",
            average_rating=0,
            total_students=0,
            total_reviews=0
        )
        self.assertEqual(course.title, "Python avancé")
        self.assertEqual(course.user, self.instructor)
        self.assertEqual(course.category, self.category)
        self.assertEqual(course.sub_category, self.subcategory)
