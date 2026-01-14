from quizquestions.models import QuizQuestion
from quizoptions.models import QuizOption
from typeresponses.models import TypeResponse
from quizs.tests.base_test_quiz import BaseQuizTest
from typequestions.models import TypeQuestion  # <-- important

class BaseQuizOptionTest(BaseQuizTest):
    """
    Base de test pour QuizOption
    """

    def setUp(self):
        super().setUp()

        # ---------- TYPE REPONSE ----------
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

        # ---------- TYPE QUESTION ----------
        self.type_question = TypeQuestion.objects.create(
            name="Multiple Choice"
        )

        # ---------- QUESTIONS ----------
        self.question_instructor = QuizQuestion.objects.create(
            quiz=self.quiz_instructor,
            question_text="Question instructor",
            type_question=self.type_question,
            points=5,
            order=1
        )

        self.question_other = QuizQuestion.objects.create(
            quiz=self.quiz_other_instructor,
            question_text="Question other",
            type_question=self.type_question,
            points=5,
            order=1
        )

    # ---------- UTILITAIRES ----------
    def create_option(self, text, question, is_correct=False):
        return QuizOption.objects.create(
            quiz_question=question,
            option_text=text,
            is_correct=is_correct,
            type_reponse=self.type_response
        )
