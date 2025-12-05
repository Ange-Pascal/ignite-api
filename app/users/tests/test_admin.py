from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from users.admin import UserAdmin
from users.models import User

class UserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_useradmin_list_display_contains_email_name_is_staff(self):
        """Verifie que user admin affiche les champs corrects dans la liste"""
        user_admin = UserAdmin(User, self.site)
        self.assertIn("email", user_admin.list_display)
        self.assertIn("name", user_admin.list_display)
        self.assertIn("is_staff", user_admin.list_display)

    def test_useradmin_add_fieldsets_contains_email_name_password(self):
        """Verifie que le formulaire d'ajout combien les bons champs"""
        user_admin = UserAdmin(User, self.site)
        add_fields = [f for fs in user_admin.add_fieldsets for f in fs[1]["fields"]]
        self.assertIn("email", add_fields)
        self.assertIn("name", add_fields)
        self.assertIn("password1", add_fields)
        self.assertIn("password2", add_fields)
