from quizquestions.models import QuizQuestion
from quizoptions.models import QuizOption
from typeresponses.models import TypeResponse
from quizs.tests.base_test_quiz import BaseQuizTest


class BaseQuizOptionTest(BaseQuizTest):
    """
    Base de test pour QuizOption
    """

    def setUp(self):
        super().setUp()

        # ---------- TYPE RESPONSE ----------
        self.type_response = TypeResponse.objects.create(
            name="single_choice"
        )

        # ---------- QUIZ ----------
        self.quiz_instructor = self.create_quiz(
            "Quiz Instructor", user=self.instructor
        )
        self.quiz_other_instructor = self.create_quiz(
            "Quiz Other", user=self.other_instructor
        )

        # ---------- QUESTIONS ----------
        self.question_instructor = QuizQuestion.objects.create(
            quiz=self.quiz_instructor,
            question_text="Question instructor",
            type_question_id=self.type_quiz.id,
            points=5,
            order=1
        )

        self.question_other = QuizQuestion.objects.create(
            quiz=self.quiz_other_instructor,
            question_text="Question other",
            type_question_id=self.type_quiz.id,
            points=5,
            order=1
        )

    # ---------- UTILITAIRES ----------
    def create_option(self, text, question, is_correct=False):
        """
        Crée une option pour une question spécifique
        """
        return QuizOption.objects.create(
            quiz_question=question,
            option_text=text,
            is_correct=is_correct,
            type_response=self.type_response  # correction ici
        )
