from rest_framework.test import APITestCase
from users.models import User
from carts.models import Cart
from cartitems.models import CartItem
from categories.models import Category
from subcategories.models import SubCategory
from courses.models import Course
from checkouts.models import Checkout
from payments.models import Payment
from paymentmethods.models import PaymentMethod
from inscriptions.models import Inscription
from payments.serializers import PaymentSerializer



class InscriptionAfterPaymentTests(APITestCase):

    def setUp(self):
        # --- Users ---
        self.user = User.objects.create_user(email="user@test.com", password="password123")

        # --- Categories ---
        self.category = Category.objects.create(name="Backend")
        self.sub_category = SubCategory.objects.create(name="Django", category=self.category)

        # --- Course ---
        self.course = Course.objects.create(
            user=self.user,
            category=self.category,
            sub_category=self.sub_category,
            title="Django API",
            slug="django-api",
            subtitle="Build APIs",
            description="desc",
            language="fr",
            level="beginner",
            price=100,
            discount_price=0,
            thumbnail="thumb.jpg",
            promo_video_url="video.mp4",
            requirements="none",
            what_you_will_learn="all",
            status="published"
        )

        # --- Cart ---
        self.cart = Cart.objects.create(user=self.user, total_amount=100)
        CartItem.objects.create(cart=self.cart, course=self.course, price=100)

        # --- Checkout ---
        self.checkout = Checkout.objects.create(user=self.user, cart=self.cart, total_amount=100)

        # --- Payment Method ---
        self.payment_method = PaymentMethod.objects.create(name="Card", code="card", is_active=True)

    def test_inscription_created_when_payment_completed(self):
        serializer = PaymentSerializer(
            data={
                "checkout": self.checkout.id,
                "payment_method": self.payment_method.id
            },
            context={"request": type("obj", (object,), {"user": self.user})()}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertEqual(Inscription.objects.count(), 1)
        inscription = Inscription.objects.first()
        self.assertEqual(inscription.user, self.user)
        self.assertEqual(inscription.course, self.course)
        self.assertEqual(inscription.status, "approved")


    def test_no_inscription_when_payment_pending(self):
        Payment.objects.create(
            user=self.user,
            checkout=self.checkout,
            payment_method=self.payment_method,
            amount=self.checkout.total_amount,
            status="pending"
        )

        self.assertEqual(Inscription.objects.count(), 0)

    def test_no_duplicate_inscription(self):
        # Premier paiement via serializer
        serializer = PaymentSerializer(
            data={
                "checkout": self.checkout.id,
                "payment_method": self.payment_method.id
            },
            context={"request": type("obj", (object,), {"user": self.user})()}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Appel simulé de création d'inscription multiple
        # Par exemple, réexécuter la logique d'inscription du serializer
        cart = self.checkout.cart
        for item in cart.items.all():
            Inscription.objects.get_or_create(
                user=self.checkout.user,
                course=item.course,
                defaults={"status": "approved"},
            )

        # Vérifie qu'il n'y a qu'une seule inscription
        self.assertEqual(Inscription.objects.count(), 1)
