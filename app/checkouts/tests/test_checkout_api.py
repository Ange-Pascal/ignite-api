from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from carts.models import Cart
from courses.models import Course
from categories.models import Category
from subcategories.models import SubCategory
from checkouts.models import Checkout
from cartitems.models import CartItem
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class CheckoutAPITests(APITestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(email="user@test.com", password="password123")
        self.other_user = User.objects.create_user(email="other@test.com", password="password123")

        # Categories
        self.category = Category.objects.create(name="Programming")
        self.sub_category = SubCategory.objects.create(name="Web Development", category=self.category)

        # Courses
        self.course = Course.objects.create(
            user=self.other_user,
            category=self.category,
            sub_category=self.sub_category,
            title="Django REST API",
            slug="django-rest-api",
            subtitle="Learn DRF",
            description="Full DRF course",
            language="English",
            level="all",
            price=100,
            discount_price=0,
            thumbnail="thumb.jpg",
            promo_video_url="promo.mp4",
            requirements="Basic Python",
            what_you_will_learn="REST APIs",
            status="published"
        )

        # Cart et CartItem
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, course=self.course, quantity=1, price=self.course.price)
        self.cart.total_amount = self.cart_item.price  # total_amount du panier
        self.cart.save()

        # URL
        self.url_list = reverse("checkout-list")

    def test_authenticated_user_can_create_checkout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        data = {"cart": self.cart.id, "payment_method": "card"}
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Checkout.objects.count(), 1)
        checkout = Checkout.objects.first()
        self.assertEqual(checkout.user, self.user)
        self.assertEqual(checkout.total_amount, self.cart.total_amount)
        self.assertEqual(checkout.payment_method, "card")
        self.assertEqual(checkout.status, "pending")

    def test_user_cannot_checkout_another_users_cart(self):
        other_cart = Cart.objects.create(user=self.other_user)
        CartItem.objects.create(cart=other_cart, course=self.course, quantity=1, price=self.course.price)
        other_cart.total_amount = self.course.price
        other_cart.save()

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        data = {"cart": other_cart.id, "payment_method": "card"}
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_unauthenticated_user_cannot_create_checkout(self):
        data = {"cart": self.cart.id, "payment_method": "card"}
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
