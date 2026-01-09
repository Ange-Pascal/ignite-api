from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from .base import BaseVideoTest

class VideoPermissionTest(BaseVideoTest):

    def test_instructor_can_create_video_on_own_course(self):
        # Création de l'instructeur et du cours
        instructor = self.create_user("instructor")
        course = self.create_course(instructor)

        # Création d'un module et d'une leçon
        module = self.create_module(course)
        lesson = self.create_lesson(module)  # ✅ on passe le module

        self.client.force_authenticate(user=instructor)

        video = SimpleUploadedFile(
            "video.mp4",
            b"fake content",
            content_type="video/mp4"
        )

        response = self.client.post(
            "/api/videos/",
            {
                "lesson": lesson.id,
                "video": video,
                "duration": 120
            },
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_instructor_cannot_create_video_on_other_course(self):
        # Création de l'instructeur test et d'un autre instructeur
        instructor = self.create_user("instructor")
        other = self.create_user("instructor")

        # Cours et leçon pour l'autre instructeur
        course = self.create_course(other)
        module = self.create_module(course)   # ✅ module pour le cours
        lesson = self.create_lesson(module)   # ✅ leçon attachée au module

        self.client.force_authenticate(user=instructor)

        video = SimpleUploadedFile(
            "video.mp4",
            b"fake content",
            content_type="video/mp4"
        )

        response = self.client.post(
            "/api/videos/",
            {
                "lesson": lesson.id,
                "video": video,
                "duration": 120
            },
            format="multipart"
        )

        # L'instructeur ne peut pas créer sur le cours d'un autre
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
