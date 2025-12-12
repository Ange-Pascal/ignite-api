from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from roles.models import Role


User = get_user_model()


class AddInstructorRoleTests(APITestCase):

    def setUp(self):
        # Créer les rôles nécessaires
        self.student_role = Role.objects.create(name="student")
        self.instructor_role = Role.objects.create(name="instructor")
        self.admin_role = Role.objects.create(name="admin")

        # Admin
        self.admin = User.objects.create_user(
            email="admin@test.com",
            password="password123",
            name="Admin User",
            is_staff=True,
            is_superuser=True
        )
        self.admin.roles.add(self.admin_role)

        # Utilisateur normal
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123",
            name="Normal User",
        )
        self.user.roles.add(self.student_role)

        self.url = reverse("user:add-instructor-role", args=[self.user.id])

    def authenticate_admin(self):
        self.client.force_authenticate(user=self.admin)

    def authenticate_user(self):
        self.client.force_authenticate(user=self.user)

    def test_admin_can_add_instructor_role(self):
        """Un admin peut ajouter le rôle instructor à un user."""
        self.authenticate_admin()

        res = self.client.post(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("instructor", [r.name for r in self.user.roles.all()])

    def test_non_admin_cannot_add_role(self):
        """Un utilisateur normal ne peut pas attribuer de rôles."""
        self.authenticate_user()

        res = self.client.post(self.url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_not_found(self):
        """Retourne 404 si l'utilisateur n'existe pas."""
        self.authenticate_admin()

        wrong_url = reverse("user:add-instructor-role", args=[999])
        res = self.client.post(wrong_url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_add_duplicate_role(self):
        """Empêche l’ajout du rôle instructor si déjà présent."""
        self.authenticate_admin()

        # Ajouter une première fois
        self.user.roles.add(self.instructor_role)

        # Refaire l’appel
        res = self.client.post(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["message"], "This user is already an instructor.")
        self.assertEqual(self.user.roles.filter(name="instructor").count(), 1)

    def test_role_is_correctly_added_to_m2m(self):
        """Vérifie que le rôle est ajouté dans la relation ManyToMany."""
        self.authenticate_admin()
        self.assertFalse(self.user.roles.filter(name="instructor").exists())

        self.client.post(self.url)

        self.assertTrue(self.user.roles.filter(name="instructor").exists())
