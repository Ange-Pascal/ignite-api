
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from quizs.models import Quiz
from typequizs.models import TypeQuiz
from roles.models import Role

User = get_user_model()


class BaseQuizTest(APITestCase):
    """
    Base pour tous les tests Quiz
    - Création d'utilisateurs : admin, instructor, autre instructor, student
    - Création d'un TypeQuiz
    - Création d'un ContentType polymorphique (Course exemple)
    """

    def setUp(self):
        # ---------- USERS ----------
        self.admin = User.objects.create_user(
            email="admin@example.com", password="pass1234", is_staff=True
        )
        self.instructor = User.objects.create_user(
            email="instructor@example.com", password="pass1234"
        )
        self.other_instructor = User.objects.create_user(
            email="instructor2@example.com", password="pass1234"
        )
        self.student = User.objects.create_user(
            email="student@example.com", password="pass1234"
        )

        # ---------- ROLES ----------
        admin_role, _ = Role.objects.get_or_create(name="admin")
        instructor_role, _ = Role.objects.get_or_create(name="instructor")
        student_role, _ = Role.objects.get_or_create(name="student")

        self.admin.roles.add(admin_role)
        self.instructor.roles.add(instructor_role)
        self.other_instructor.roles.add(instructor_role)

        # ---------- TYPE QUIZ ----------
        self.type_quiz = TypeQuiz.objects.create(name="Diagnostic")

        # ---------- CONTENT TYPE ----------
        class DummyCourse:
            id = 1
        self.course_content_type = ContentType.objects.create(
            app_label="quizzes", model="dummycourse"
        )


    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_client(self, user):
        token = self.get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class QuizCRUDTests(BaseQuizTest):
    """Tests CRUD pour le Quiz avec rôles Admin / Instructor"""

    # --------------------- LIST ---------------------
    def test_list_quiz_admin_sees_all(self):
        Quiz.objects.create(
            title="Quiz 1",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        Quiz.objects.create(
            title="Quiz 2",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.other_instructor,
        )
        self.auth_client(self.admin)
        url = reverse("quiz-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test_list_quiz_instructor_sees_only_their_quiz(self):
        quiz1 = Quiz.objects.create(
            title="Quiz 1",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        Quiz.objects.create(
            title="Quiz 2",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.other_instructor,
        )
        self.auth_client(self.instructor)
        url = reverse("quiz-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], quiz1.id)

    def test_list_quiz_student_sees_none(self):
        Quiz.objects.create(
            title="Quiz 1",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        self.auth_client(self.student)
        url = reverse("quiz-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 0)

    # --------------------- CREATE ---------------------
    def test_create_quiz_admin_success(self):
        self.auth_client(self.admin)
        url = reverse("quiz-list")
        data = {
            "title": "Quiz Admin",
            "type_quiz": self.type_quiz.id,
            "passing_score": 70,
            "max_attempts": 3,
            "time_limit": 30,
            "shuffle_questions": True,
            "shuffle_options": True,
            "status": "draft",
            "quizable_type": self.course_content_type.id,
            "quizable_id": 1,
        }
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["title"], "Quiz Admin")

    def test_create_quiz_instructor_success(self):
        self.auth_client(self.instructor)
        url = reverse("quiz-list")
        data = {
            "title": "Quiz Instructor",
            "type_quiz": self.type_quiz.id,
            "passing_score": 60,
            "max_attempts": 2,
            "time_limit": 20,
            "shuffle_questions": False,
            "shuffle_options": False,
            "status": "draft",
            "quizable_type": self.course_content_type.id,
            "quizable_id": 1,
        }
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["title"], "Quiz Instructor")

    def test_create_quiz_student_forbidden(self):
        self.auth_client(self.student)
        url = reverse("quiz-list")
        data = {"title": "Quiz Student"}
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, 403)

    # --------------------- RETRIEVE ---------------------
    def test_retrieve_quiz_owner_or_admin(self):
        quiz = Quiz.objects.create(
            title="Q1",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        # Owner
        self.auth_client(self.instructor)
        url = reverse("quiz-detail", args=[quiz.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

        # Admin
        self.auth_client(self.admin)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_retrieve_quiz_student_forbidden(self):
        quiz = Quiz.objects.create(
            title="Q1",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        self.auth_client(self.student)
        url = reverse("quiz-detail", args=[quiz.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

    # --------------------- UPDATE ---------------------
    def test_update_quiz_owner_success(self):
        quiz = Quiz.objects.create(
            title="Old Title",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        self.auth_client(self.instructor)
        url = reverse("quiz-detail", args=[quiz.id])
        data = {
            "title": "New Title",
            "type_quiz": self.type_quiz.id,
            "passing_score": 60,
            "max_attempts": 1,
            "time_limit": 10,
            "shuffle_questions": False,
            "shuffle_options": False,
            "status": "published",
            "quizable_type": self.course_content_type.id,
            "quizable_id": 1,
        }
        res = self.client.put(url, data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["title"], "New Title")

    def test_update_quiz_not_owner_forbidden(self):
        quiz = Quiz.objects.create(
            title="Other Quiz",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.other_instructor,
        )
        self.auth_client(self.instructor)
        url = reverse("quiz-detail", args=[quiz.id])
        data = {"title": "Hack"}
        res = self.client.put(url, data, format="json")
        self.assertEqual(res.status_code, 403)

    # --------------------- DELETE ---------------------
    def test_delete_quiz_owner_success(self):
        quiz = Quiz.objects.create(
            title="To Delete",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.instructor,
        )
        self.auth_client(self.instructor)
        url = reverse("quiz-detail", args=[quiz.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Quiz.objects.filter(id=quiz.id).exists())

    def test_delete_quiz_not_owner_forbidden(self):
        quiz = Quiz.objects.create(
            title="Other Quiz",
            type_quiz=self.type_quiz,
            passing_score=50,
            quizable_type=self.course_content_type,
            quizable_id=1,
            created_by=self.other_instructor,
        )
        self.auth_client(self.instructor)
        url = reverse("quiz-detail", args=[quiz.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 403)
