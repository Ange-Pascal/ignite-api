from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from instructors.models import InstructorProfile

PROFILE_LIST_URL = reverse("instructor:profile-list")
def profile_detail_url(profile_id):
    return reverse("instructor:profile-detail", args=[profile_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


class PublicInstructorProfileTests(APITestCase):
    """Tests accès public interdit"""

    def test_cannot_access_profile_list(self):
        res = self.client.get(PROFILE_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInstructorProfileTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="pass123", name="User Name")
        self.superuser = create_superuser(email="admin@example.com", password="admin123")

        self.client.force_authenticate(self.user)

    def test_create_instructor_profile(self):
        payload = {
            "bio": "Je suis développeur",
            "experience": "5 ans",
            "links": "http://github.com/user"
        }
        res = self.client.post(PROFILE_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        profile = InstructorProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, payload["bio"])
        self.assertEqual(profile.experience, payload["experience"])

    def test_user_can_update_own_profile(self):
        profile = InstructorProfile.objects.create(
            user=self.user,
            bio="Ancienne bio",
            experience="2 ans",
            links=""
        )
        payload = {"bio": "Nouvelle bio"}
        url = profile_detail_url(profile.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.bio, payload["bio"])

    def test_user_cannot_update_other_profile(self):
        other = create_user(email="other@example.com", password="pass123")
        profile = InstructorProfile.objects.create(user=other, bio="Bio", experience="1 an", links="")
        url = profile_detail_url(profile.id)
        res = self.client.patch(url, {"bio": "Hacked"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_delete_any_profile(self):
        profile = InstructorProfile.objects.create(user=self.user, bio="Bio", experience="1 an", links="")
        self.client.force_authenticate(self.superuser)
        url = profile_detail_url(profile.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(InstructorProfile.objects.filter(id=profile.id).exists())
