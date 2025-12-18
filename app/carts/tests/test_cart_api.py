from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from carts.models import Cart
from rest_framework_simplejwt.tokens import RefreshToken

def get_token(user):
    return str(RefreshToken.for_user(user).access_token)

class CartAPITests(APITestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(
            email="user@test.com", password="password123"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com", password="password123"
        )

        # URL list et detail
        self.url_list = reverse("cart-list")

    # ✅ Création d’un cart actif
    def test_authenticated_user_can_create_cart(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )
        response = self.client.post(self.url_list, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.first().user, self.user)
        self.assertEqual(Cart.objects.first().status, "active")

    # ❌ Interdire plusieurs carts actifs
    def test_user_cannot_create_multiple_active_carts(self):
        Cart.objects.create(user=self.user, status="active")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )
        response = self.client.post(self.url_list, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Cart.objects.filter(user=self.user).count(), 1)

    # 🔒 Un utilisateur ne voit que ses propres carts
    def test_user_can_only_see_own_carts(self):
        Cart.objects.create(user=self.other_user, status="active")
        Cart.objects.create(user=self.user, status="active")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"], self.user.id)

    # ❌ Accès non authentifié interdit
    def test_unauthenticated_user_cannot_access_cart(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ✅ Détail d’un cart
    def test_authenticated_user_can_retrieve_cart_detail(self):
        cart = Cart.objects.create(user=self.user)
        url_detail = reverse("cart-detail", args=[cart.id])
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], cart.id)

    # ✅ Mise à jour d’un cart
    def test_authenticated_user_can_update_cart_status(self):
        cart = Cart.objects.create(user=self.user)
        url_detail = reverse("cart-detail", args=[cart.id])
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )
        response = self.client.patch(url_detail, {"status": "checked_out"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart.refresh_from_db()
        self.assertEqual(cart.status, "checked_out")

    # ✅ Suppression d’un cart
    def test_authenticated_user_can_delete_cart(self):
        cart = Cart.objects.create(user=self.user)
        url_detail = reverse("cart-detail", args=[cart.id])
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {get_token(self.user)}"
        )
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(id=cart.id).exists())
