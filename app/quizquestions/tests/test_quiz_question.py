from rest_framework import status
from rest_framework.reverse import reverse
from quizquestions.models import QuizQuestion
from quizs.models import TypeQuiz
from quizquestions.tests.base_test_quiz_question import BaseQuizQuestionTest  # <-- utiliser le bon BaseTest


class QuizQuestionApiTest(BaseQuizQuestionTest):
    """
    Test CRUD QuizQuestion avec TDD
    - Admin : accès total
    - Instructor : CRUD sur ses quiz
    - Student : aucun accès
    """
    def setUp(self):
        super().setUp()

        # Créons un quiz pour l'instructor
        self.quiz_instructor = self.create_quiz(
            title="Quiz Instructor",
            user=self.instructor,
            type_quiz=self.type_quiz
        )

        self.quiz_other_instructor = self.create_quiz(
            title="Quiz Autre Instructor",
            user=self.other_instructor,
            type_quiz=self.type_quiz
        )

        # URL du endpoint QuizQuestion
        self.url = reverse('quiz-question-list')

    # ------------------- CREATE -------------------
    def test_instructor_can_create_own_quiz_question(self):
        self.auth_client(self.instructor)
        data = {
            "quiz_id": self.quiz_instructor.id,
            "question_text": "Question test 1",
            "type_question_id": self.type_question.id,  # <-- corrige ici
            "points": 5,
            "order": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(QuizQuestion.objects.filter(quiz=self.quiz_instructor).count(), 1)

    def test_instructor_cannot_create_question_on_other_quiz(self):
        self.auth_client(self.instructor)
        data = {
            "quiz_id": self.quiz_other_instructor.id,
            "question_text": "Question interdite",
            "type_question_id": self.type_question.id,
            "points": 5,
            "order": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_question_on_any_quiz(self):
        self.auth_client(self.admin)
        data = {
            "quiz_id": self.quiz_other_instructor.id,
            "question_text": "Question admin",
            "type_question_id": self.type_question.id,
            "points": 5,
            "order": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_question(self):
        self.auth_client(self.student)
        data = {
            "quiz_id": self.quiz_instructor.id,
            "question_text": "Student question",
            "type_question_id": self.type_question.id,
            "points": 5,
            "order": 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------- LIST -------------------
    def test_instructor_sees_only_own_quiz_questions(self):
        self.create_quiz_question("Q1", self.quiz_instructor)
        self.create_quiz_question("Q2", self.quiz_other_instructor)

        self.auth_client(self.instructor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question_text'], "Q1")

    def test_admin_sees_all_questions(self):
        self.create_quiz_question("Q1", self.quiz_instructor)
        self.create_quiz_question("Q2", self.quiz_other_instructor)

        self.auth_client(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ------------------- RETRIEVE -------------------
    def test_instructor_can_retrieve_own_question(self):
        q = self.create_quiz_question("Q1", self.quiz_instructor)
        self.auth_client(self.instructor)
        url = reverse('quiz-question-detail', args=[q.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question_text'], "Q1")

    def test_instructor_cannot_retrieve_other_question(self):
        q = self.create_quiz_question("Q2", self.quiz_other_instructor)
        self.auth_client(self.instructor)
        url = reverse('quiz-question-detail', args=[q.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------- UPDATE -------------------
    def test_instructor_can_update_own_question(self):
        q = self.create_quiz_question("Q1", self.quiz_instructor)
        self.auth_client(self.instructor)
        url = reverse('quiz-question-detail', args=[q.id])
        data = {"question_text": "Q1 modifiée"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        q.refresh_from_db()
        self.assertEqual(q.question_text, "Q1 modifiée")

    def test_instructor_cannot_update_other_question(self):
        q = self.create_quiz_question("Q2", self.quiz_other_instructor)
        self.auth_client(self.instructor)
        url = reverse('quiz-question-detail', args=[q.id])
        data = {"question_text": "Modification interdite"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------- DELETE -------------------
    def test_instructor_can_delete_own_question(self):
        q = self.create_quiz_question("Q1", self.quiz_instructor)
        self.auth_client(self.instructor)
        url = reverse('quiz-question-detail', args=[q.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(QuizQuestion.objects.filter(id=q.id).exists())

    def test_instructor_cannot_delete_other_question(self):
        q = self.create_quiz_question("Q2", self.quiz_other_instructor)
        self.auth_client(self.instructor)
        url = reverse('quiz-question-detail', args=[q.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------- UTILITAIRE -------------------
    def create_quiz_question(self, text, quiz):
        return QuizQuestion.objects.create(
            quiz=quiz,
            type_question=self.type_question,  # <-- corrigé ici
            question_text=text,
            points=5,
            order=1
        )
