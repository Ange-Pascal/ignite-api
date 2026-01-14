from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from quizs.models import Quiz, TypeQuiz
from quizquestions.models import QuizQuestion
from typequestions.models import TypeQuestion
from roles.models import Role

User = get_user_model()


class BaseQuizQuestionTest(APITestCase):
    """
    Base Test pour les tests liés à QuizQuestion
    Fournit :
    - Users : admin, instructor, student
    - JWT authentification
    - TypeQuiz et TypeQuestion par défaut
    - Création rapide de Quiz et QuizQuestion
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

        # Assignation des rôles
        self.admin.roles.add(admin_role, student_role)  # si tu veux que l'admin puisse aussi être étudiant
        self.instructor.roles.add(instructor_role, student_role)  # si tes instructeurs doivent pouvoir avoir le rôle student
        self.other_instructor.roles.add(instructor_role)
        self.student.roles.add(student_role)

        # ---------- TYPE QUIZ ----------
        self.type_quiz, _ = TypeQuiz.objects.get_or_create(name="Diagnostic")

        # ---------- TYPE QUESTION ----------
        self.type_question, _ = TypeQuestion.objects.get_or_create(name="QCM")

        # ---------- CONTENT TYPE ----------
        # Crée un ContentType fictif pour le quizable
        class DummyCourse:
            id = 1
        self.course_content_type = ContentType.objects.get_or_create(
            app_label="quizzes", model="dummycourse"
        )[0]

    # ---------- JWT ----------
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def auth_client(self, user):
        token = self.get_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # ---------- UTILITAIRES ----------
    def create_quiz(self, title, user=None, type_quiz=None):
        if user is None:
            user = self.instructor
        if type_quiz is None:
            type_quiz = self.type_quiz
        return Quiz.objects.create(
            title=title,
            type_quiz=type_quiz,
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

    def create_quiz_question(self, quiz=None, type_question=None, text="Question test", points=5, order=1):
        if quiz is None:
            quiz = self.create_quiz("Quiz par défaut")
        if type_question is None:
            type_question = self.type_question
        return QuizQuestion.objects.create(
            quiz=quiz,
            type_question=type_question,
            question_text=text,
            points=points,
            order=order
        )
