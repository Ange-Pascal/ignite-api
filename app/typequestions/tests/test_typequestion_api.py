from rest_framework import status
from typequestions.models import TypeQuestion
from typequestions.tests.base import BaseTypeQuestionTest


class TypeQuestionApiTest(BaseTypeQuestionTest):

    def test_public_can_list_typequestion(self):
        """
        Lecture publique, même par un user non authentifié
        """
        TypeQuestion.objects.create(name="Diagnostic")

        response = self.client.get("/api/type-questions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_typequestion(self):
        """
        Un admin peut créer un type de quiz
        """
        admin = self.create_user("admin")

        # On force l'authentification
        self.client.force_authenticate(user=admin)

        response = self.client.post(
            "/api/type-questions/",
            {"name": "Formatif", "description": "Quiz de progression"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TypeQuestion.objects.count(), 1)

    def test_instructor_cannot_create_typequestion(self):
        """
        Les instructeurs ne peuvent pas créer de quiz
        """
        instructor = self.create_user("instructor")
        self.client.force_authenticate(user=instructor)

        response = self.client.post("/api/type-questions/", {"name": "Sommatif"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_typequestion(self):
        """
        L'admin peut mettre à jour un typequiz
        """
        admin = self.create_user("admin")
        question_type = TypeQuestion.objects.create(name="Certif")
        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/type-questions/{question_type.id}/",
            {"name": "Certificatif"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        question_type.refresh_from_db()
        self.assertEqual(question_type.name, "Certificatif")

    def test_admin_can_delete_typequestion(self):
        """
        L'admin peut supprimer un typequiz
        """
        admin = self.create_user("admin")
        question_type = TypeQuestion.objects.create(name="Diagnostic")
        self.client.force_authenticate(user=admin)

        response = self.client.delete(f"/api/type-questions/{question_type.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_cannot_create(self):
        """
        Un user non authentifié ne peut pas créer de type quiz
        """
        response = self.client.post("/api/type-questions/", {"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
