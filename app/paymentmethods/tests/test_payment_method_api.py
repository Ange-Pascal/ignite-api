from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from paymentmethods.models import PaymentMethod
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)

class PaymentMethodAPITests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@test.com", password="password123")
        self.user = User.objects.create_user(email="user@test.com", password="password123")
        self.url_list = reverse("paymentmethod-list")

    def test_admin_can_create_payment_method(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.admin)}")
        data = {"name": "Card", "code": "card", "fee_percent": 1.5}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PaymentMethod.objects.count(), 1)

    def test_non_admin_cannot_create_payment_method(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        data = {"name": "PayPal", "code": "paypal", "fee_percent": 2}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_only_active_payment_methods(self):
        PaymentMethod.objects.create(name="Card", code="card", is_active=True)
        PaymentMethod.objects.create(name="PayPal", code="paypal", is_active=False)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
