from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from carts.models import Cart
from checkouts.models import Checkout
from payments.models import Payment
from paymentmethods.models import PaymentMethod
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class PaymentAPITests(APITestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(
            email="user@test.com",
            password="password123"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="password123"
        )

        # Cart
        self.cart = Cart.objects.create(
            user=self.user,
            total_amount=100
        )

        # Checkout
        self.checkout = Checkout.objects.create(
            user=self.user,
            cart=self.cart,
            total_amount=100,
            status="pending"
        )

        # Payment Method
        self.payment_method = PaymentMethod.objects.create(
            name="Card",
            code="card",
            is_active=True
        )

        self.url_list = reverse("payment-list")

    # ✅ SUCCESS
    def test_authenticated_user_can_pay_own_checkout(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )

        data = {
            "checkout": self.checkout.id,
            "payment_method": self.payment_method.id
        }

        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)

        payment = Payment.objects.first()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount, self.checkout.total_amount)
        self.assertEqual(payment.status, "pending")

    # ❌ SECURITY
    def test_user_cannot_pay_another_users_checkout(self):
        other_cart = Cart.objects.create(
            user=self.other_user,
            total_amount=50
        )
        other_checkout = Checkout.objects.create(
            user=self.other_user,
            cart=other_cart,
            total_amount=50,
            status="pending"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )

        data = {
            "checkout": other_checkout.id,
            "payment_method": self.payment_method.id
        }

        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Payment.objects.count(), 0)

    # ❌ AUTH
    def test_unauthenticated_user_cannot_pay(self):
        data = {
            "checkout": self.checkout.id,
            "payment_method": self.payment_method.id
        }

        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ❌ BUSINESS RULE
    def test_cannot_pay_completed_checkout(self):
        self.checkout.status = "completed"
        self.checkout.save()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )

        data = {
            "checkout": self.checkout.id,
            "payment_method": self.payment_method.id
        }

        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Payment.objects.count(), 0)

    # ✅ SIDE EFFECT (PRO)
    def test_completed_payment_marks_checkout_as_completed(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )

        # 1️⃣ create payment
        response = self.client.post(
            self.url_list,
            {
                "checkout": self.checkout.id,
                "payment_method": self.payment_method.id
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payment = Payment.objects.first()

        # 2️⃣ simulate provider confirmation
        payment.status = "completed"
        payment.save()

        self.checkout.refresh_from_db()
        self.assertEqual(self.checkout.status, "completed")
