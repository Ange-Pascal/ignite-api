from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """Test de la creation d'un user"""


    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))


    def test_new_user_normilized(self):
        """Transoformer les emails en miniscule avant de les envoyer"""


        email= "Test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email, "pass123")
        self.assertEqual(user.email, "test@example.com")

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "super@example.com",
            "pass123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

