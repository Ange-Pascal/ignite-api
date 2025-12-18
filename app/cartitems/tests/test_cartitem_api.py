# cartitems/tests/test_cartitem_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from carts.models import Cart
from cartitems.models import CartItem
from courses.models import Course
from categories.models import Category
from subcategories.models import SubCategory
from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    return str(RefreshToken.for_user(user).access_token)


class CartItemAPITests(APITestCase):

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

        # Categories / SubCategories
        self.category = Category.objects.create(name="Programming")
        self.sub_category = SubCategory.objects.create(
            name="Backend",
            category=self.category
        )

        # Course
        self.course = Course.objects.create(
            user=self.other_user,
            category=self.category,
            sub_category=self.sub_category,
            title="Django REST API",
            slug="django-rest-api",
            subtitle="DRF",
            description="Learn DRF",
            language="English",
            level="beginner",
            price=100,
            discount_price=50,
            thumbnail="thumb.jpg",
            promo_video_url="https://youtube.com/test",
            requirements="Python",
            what_you_will_learn="Build APIs",
            status="published",
        )

        # Cart
        self.cart = Cart.objects.create(user=self.user)

        # URL
        self.url = reverse("cart-items-list")

    # ✅ Authenticated user can add course to cart
    def test_authenticated_user_can_add_course_to_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        data = {"course": self.course.id}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().cart, self.cart)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_amount, self.course.price)

    # ❌ Same course cannot be added twice
    def test_user_cannot_add_same_course_twice(self):
        CartItem.objects.create(cart=self.cart, course=self.course, price=self.course.price)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        response = self.client.post(self.url, {"course": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CartItem.objects.count(), 1)

    # 🔒 User sees only own cart items
    def test_user_can_only_see_his_cart_items(self):
        other_cart = Cart.objects.create(user=self.other_user)
        CartItem.objects.create(cart=other_cart, course=self.course, price=self.course.price)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # 🚫 Unauthenticated user forbidden
    def test_unauthenticated_user_cannot_access_cart_items(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_post = self.client.post(self.url, {"course": self.course.id})
        self.assertEqual(response_post.status_code, status.HTTP_401_UNAUTHORIZED)

    # 🗑 Auth user can remove course from cart
    def test_authenticated_user_can_remove_course_from_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, course=self.course, price=self.course.price)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}")
        url_delete = reverse("cart-items-detail", args=[cart_item.id])

        response = self.client.delete(url_delete)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.total_amount, 0)
