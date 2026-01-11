from rest_framework import status
from typeresponses.models import TypeResponse
from typeresponses.tests.base import BaseTypeResponseTest


class TypeQuestionApiTest(BaseTypeResponseTest):

    def test_public_can_list_typeresponse(self):
        """
        Lecture publique, même par un user non authentifié
        """
        TypeResponse.objects.create(name="Project")

        response = self.client.get("/api/type-responses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_typeresponse(self):
        """
        Un admin peut créer un type de response
        """
        admin = self.create_user("admin")

        # On force l'authentification
        self.client.force_authenticate(user=admin)

        response = self.client.post(
            "/api/type-responses/",
            {"name": "Project", "description": "Televerser son projet"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TypeResponse.objects.count(), 1)

    def test_instructor_cannot_create_typeresponse(self):
        """
        Les instructeurs ne peuvent pas créer de type response
        """
        instructor = self.create_user("instructor")
        self.client.force_authenticate(user=instructor)

        response = self.client.post("/api/type-responses/", {"name": "QCM"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_typeresponse(self):
        """
        L'admin peut mettre à jour un type response
        """
        admin = self.create_user("admin")
        response_type = TypeResponse.objects.create(name="QC")
        self.client.force_authenticate(user=admin)

        response = self.client.patch(
            f"/api/type-responses/{response_type.id}/",
            {"name": "QCM"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_type.refresh_from_db()
        self.assertEqual(response_type.name, "QCM")

    def test_admin_can_delete_typequestion(self):
        """
        L'admin peut supprimer un typequiz
        """
        admin = self.create_user("admin")
        response_type = TypeResponse.objects.create(name="Diagnostic")
        self.client.force_authenticate(user=admin)

        response = self.client.delete(f"/api/type-responses/{response_type.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_cannot_create(self):
        """
        Un user non authentifié ne peut pas créer de type responses
        """
        response = self.client.post("/api/type-responses/", {"name": "Test"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
