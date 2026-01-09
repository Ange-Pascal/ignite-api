from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from .base import BaseVideoTest
from videos.models import Video

class VideoCRUDTest(BaseVideoTest):

    def setUp(self):
        super().setUp()
        # Créer un admin et deux instructeurs pour réutilisation
        self.admin = self.create_user("admin")
        self.instructor1 = self.create_user("instructor")
        self.instructor2 = self.create_user("instructor")

    def test_admin_can_delete_any_video(self):
        # Cours, module, leçon
        course = self.create_course(self.instructor1)
        module = self.create_module(course)
        lesson = self.create_lesson(module)

        # Vidéo
        video = Video.objects.create(
            lesson=lesson,
            uploaded_file=SimpleUploadedFile("video.mp4", b"fake content", content_type="video/mp4"),
            duration=60,
            provider="local"
        )

        # Authentification admin
        self.client.force_authenticate(user=self.admin)

        # DELETE
        response = self.client.delete(f"/api/videos/{video.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Video.objects.filter(id=video.id).exists())  # ✅ Vérification suppression

    def test_instructor_cannot_delete_other_video(self):
        # Cours et vidéo de l'autre instructeur
        course = self.create_course(self.instructor2)
        module = self.create_module(course)
        lesson = self.create_lesson(module)
        video = Video.objects.create(
            lesson=lesson,
            uploaded_file=SimpleUploadedFile("video.mp4", b"fake content", content_type="video/mp4"),
            duration=60,
            provider="local"
        )

        # Authentification instructeur non propriétaire
        self.client.force_authenticate(user=self.instructor1)

        # DELETE
        response = self.client.delete(f"/api/videos/{video.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Video.objects.filter(id=video.id).exists())  # ✅ La vidéo doit rester

