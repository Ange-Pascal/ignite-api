from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from roles.models import Role
import sys

User = get_user_model()

class Command(BaseCommand):
    help = 'Diagnostic du seeding'

    def handle(self, *args, **options):
        self.stdout.write("--- DEBUT DU DIAGNOSTIC ---")

        try:
            # Étape 1 : Vérifier les rôles
            self.stdout.write("1. Vérification des rôles...")
            admin_role, created_r = Role.objects.get_or_create(name='admin')
            self.stdout.write(f"   Rôle admin: {'Créé' if created_r else 'Déjà existant'}")

            # Étape 2 : Tentative de création
            email = "admin@ignite.com"
            self.stdout.write(f"2. Tentative sur l'utilisateur: {email}")

            user, created_u = User.objects.update_or_create(
                email=email,
                defaults={
                    'name': 'Admin Diagnostic',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            self.stdout.write(f"   Utilisateur: {'Créé' if created_u else 'Mis à jour'}")

            # Étape 3 : Le Hashage (Le moment critique)
            self.stdout.write("3. Hashage du mot de passe...")
            user.set_password("password123")
            user.save()
            self.stdout.write("   Mot de passe enregistré.")

            # Étape 4 : Attribution du rôle
            self.stdout.write("4. Attribution du rôle...")
            user.roles.add(admin_role)
            self.stdout.write(f"   Rôles actuels de l'user: {[r.name for r in user.roles.all()]}")

            # Étape 5 : Test d'authentification immédiat (interne)
            self.stdout.write("5. Test d'authentification interne...")
            from django.contrib.auth import authenticate
            test_auth = authenticate(username=email, password="password123")

            if test_auth:
                self.stdout.write(self.style.SUCCESS("✅ SUCCÈS : L'utilisateur est authentifiable !"))
            else:
                self.stdout.write(self.style.ERROR("❌ ÉCHEC : L'utilisateur existe mais Django rejette le password."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"💥 CRASH DU SCRIPT : {str(e)}"))

        self.stdout.write("--- FIN DU DIAGNOSTIC ---")
