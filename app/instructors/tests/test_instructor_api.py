from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from roles.models import Role
from instructors.models import InstructorProfile
from rest_framework import status

class InstructorProfileTests(APITestCase):

    def setUp(self):
        # -----------------------------
        # Création des rôles
        # -----------------------------
        self.role_instructor = Role.objects.create(name="instructor")
        self.role_admin = Role.objects.create(name="admin")
        self.role_student = Role.objects.create(name="student")

        # -----------------------------
        # Création des utilisateurs
        # -----------------------------
        self.instructor = User.objects.create_user(
            email="instructor@test.com", password="pass123"
        )
        self.instructor.roles.add(self.role_instructor)

        self.admin = User.objects.create_user(
            email="admin@test.com", password="pass123"
        )
        self.admin.roles.add(self.role_admin)

        self.student = User.objects.create_user(
            email="student@test.com", password="pass123"
        )
        self.student.roles.add(self.role_student)

        # -----------------------------
        # Création d'un profil instructeur existant
        # -----------------------------
        self.profile = InstructorProfile.objects.create(
            user=self.instructor,
            bio="Bio test",
            experience="Expérience test",
            links="http://example.com"
        )

        # -----------------------------
        # URL pour le endpoint
        # -----------------------------
        self.list_url = reverse("instructor:instructorprofile-list")  # DefaultRouter + namespace

    # -----------------------------
    # Test création par instructeur
    # -----------------------------
    def test_instructor_cannot_create_duplicate_profile(self):
        """Un utilisateur ne peut pas créer un profil s'il en a déjà un"""
        client = APIClient()
        client.force_authenticate(user=self.instructor)
        data = {"bio": "Nouvelle bio"}
        response = client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(InstructorProfile.objects.filter(user=self.instructor).count(), 1)

    # -----------------------------
    # Test création par non-instructeur
    # -----------------------------
    def test_non_instructor_cannot_create_profile(self):
        client = APIClient()
        client.force_authenticate(user=self.student)
        data = {"bio": "Bio test"}
        response = client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(InstructorProfile.objects.filter(user=self.student).exists())

    # -----------------------------
    # Test mise à jour de son propre profil
    # -----------------------------
    def test_instructor_can_update_own_profile(self):
        client = APIClient()
        client.force_authenticate(user=self.instructor)
        url = reverse("instructor:instructorprofile-detail", args=[self.profile.id])
        data = {"bio": "Bio mise à jour", "experience": "Nouvelle expérience", "links": "http://updated.com"}
        response = client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, "Bio mise à jour")
        self.assertEqual(self.profile.experience, "Nouvelle expérience")
        self.assertEqual(self.profile.links, "http://updated.com")

    # -----------------------------
    # Test mise à jour d'un autre profil
    # -----------------------------
    def test_instructor_cannot_update_other_profile(self):
        other_instructor = User.objects.create_user(email="other@test.com", password="pass123")
        other_instructor.roles.add(self.role_instructor)
        other_profile = InstructorProfile.objects.create(user=other_instructor, bio="Autre bio")

        client = APIClient()
        client.force_authenticate(user=self.instructor)
        url = reverse("instructor:instructorprofile-detail", args=[other_profile.id])
        data = {"bio": "Tentative modification"}
        response = client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # Test admin peut modifier n'importe quel profil
    # -----------------------------
    def test_admin_can_update_any_profile(self):
        client = APIClient()
        client.force_authenticate(user=self.admin)
        url = reverse("instructor:instructorprofile-detail", args=[self.profile.id])
        data = {"bio": "Admin update", "experience": "Admin exp", "links": "http://admin.com"}
        response = client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, "Admin update")
        self.assertEqual(self.profile.experience, "Admin exp")
        self.assertEqual(self.profile.links, "http://admin.com")
