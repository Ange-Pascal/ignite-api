from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from quizs.models import Quiz
from typequizs.models import TypeQuiz
from roles.models import Role

User = get_user_model()

class BaseQuizTest(APITestCase):
    def setUp(self):
        # ---------- ROLES ----------
        self.admin_role, _ = Role.objects.get_or_create(name="admin")
        self.instructor_role, _ = Role.objects.get_or_create(name="instructor")
        self.student_role, _ = Role.objects.get_or_create(name="student")

        # ---------- USERS ----------
        self.admin = User.objects.create_user(
            email="admin@example.com", password="pass1234", is_staff=True
        )
        self.admin.roles.add(self.admin_role)

        self.instructor = User.objects.create_user(
            email="instructor@example.com", password="pass1234"
        )
        self.instructor.roles.add(self.instructor_role)

        self.other_instructor = User.objects.create_user(
            email="instructor2@example.com", password="pass1234"
        )
        self.other_instructor.roles.add(self.instructor_role)

        self.student = User.objects.create_user(
            email="student@example.com", password="pass1234"
        )
        self.student.roles.add(self.student_role)

        # ---------- TYPE QUIZ ----------
        self.type_quiz = TypeQuiz.objects.create(name="Diagnostic")

        # ---------- CONTENT TYPE ----------
        class DummyCourse:
            id = 1
        self.course_content_type = ContentType.objects.create(
            app_label="quizzes", model="dummycourse"
        )

    # ---------- JWT ----------
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_client(self, user):
        token = self.get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # ---------- UTILITAIRES ----------
    def create_quiz(self, title, user=None):
        if user is None:
            user = self.instructor
        return Quiz.objects.create(
            title=title,
            type_quiz=self.type_quiz,
            passing_score=50,
            max_attempts=3,
            time_limit=30,
            shuffle_questions=True,
            shuffle_options=True,
            status="draft",
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=user,
        )
