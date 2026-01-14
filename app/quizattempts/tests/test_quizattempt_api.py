# quizattempts/tests/test_quizattempt_api.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from quizs.models import Quiz
from quizattempts.models import QuizAttempt
from roles.models import Role
from typequizs.models import TypeQuiz

User = get_user_model()


class BaseQuizAttemptTest(APITestCase):
    def setUp(self):
        # ---------- ROLES ----------
        self.admin_role, _ = Role.objects.get_or_create(name="admin")
        self.student_role, _ = Role.objects.get_or_create(name="student")

        # ---------- USERS ----------
        self.admin = User.objects.create_user(
            email="admin@example.com", password="pass1234", is_staff=True
        )
        self.student = User.objects.create_user(email="student@example.com", password="pass1234")
        self.other_student = User.objects.create_user(email="student2@example.com", password="pass1234")

        self.admin.roles.add(self.admin_role)
        self.student.roles.add(self.student_role)
        self.other_student.roles.add(self.student_role)

        # ---------- TYPE QUIZ ----------
        self.type_quiz = TypeQuiz.objects.create(name="Test Type Quiz")

        # ---------- QUIZ ----------
        self.quiz = Quiz.objects.create(
            title="Quiz TDD",
            type_quiz=self.type_quiz,  # FK corrigée
            passing_score=50,
            max_attempts=3,
            time_limit=30,
            shuffle_questions=True,
            shuffle_options=True,
            status="published",
            quizable_type_id=1,
            quizable_id=1,
            created_by=self.admin,
        )

    # ---------- JWT ----------
    def get_token(self, user):

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_client(self, user):
        token = self.get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class QuizAttemptAPITest(BaseQuizAttemptTest):

    def test_student_can_start_quiz_creates_attempt(self):
        self.auth_client(self.student)
        url = reverse("quiz-attempt-start-quiz")
        response = self.client.post(url, data={"quiz_id": self.quiz.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            QuizAttempt.objects.filter(user=self.student, quiz=self.quiz).count(), 1
        )

        attempt = QuizAttempt.objects.get(user=self.student, quiz=self.quiz)
        self.assertEqual(attempt.status, "in_progress")
        self.assertIsNotNone(attempt.started_at)

    def test_student_get_existing_in_progress_attempt(self):
        existing_attempt = QuizAttempt.objects.create(
            quiz=self.quiz,
            user=self.student,
            status="in_progress",
            started_at="2026-01-14T00:00:00Z"
        )

        self.auth_client(self.student)
        url = reverse("quiz-attempt-start-quiz")
        response = self.client.post(url, data={"quiz_id": self.quiz.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], existing_attempt.id)
        self.assertEqual(
            QuizAttempt.objects.filter(user=self.student, quiz=self.quiz).count(), 1
        )

    def test_non_student_cannot_start_quiz(self):
        """
        Un utilisateur sans rôle student ne peut pas démarrer le quiz
        """
        # Création d'un user sans rôle
        temp_user = User.objects.create_user(email="temp@example.com", password="pass1234")
        temp_user.roles.clear()  # s'assurer qu'il n'a aucun rôle
        self.auth_client(temp_user)

        url = reverse("quiz-attempt-start-quiz")
        response = self.client.post(url, data={"quiz_id": self.quiz.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(QuizAttempt.objects.filter(user=temp_user).count(), 0)
