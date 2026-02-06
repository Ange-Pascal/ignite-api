from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from roles.models import Role

User = get_user_model()

class Command(BaseCommand):
    help = 'Créé les roles et les users par defaut( Admin, Instructor, Student)'

    def handle(self, *args, **kwargs):
        # Definir les roles
        roles_to_ensure = ['admin', 'instructor', 'student']
        role_objs = {}
        for role_name in roles_to_ensure:
            role, created = Role.objects.get_or_create(name=role_name)
            role_objs[role_name] = role
            if created:
                self.stdout.write(f"Rôle créé : {role_name}")


        # Liste des users à créer
        users_data = [
            {
                "email": "admin@ignite.com",
                "name": "Directeur",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True
            },

            {
                "email": "instructor@ignite.com",
                "name": "Akoumoua",
                "role": "instructor",
                "is_staff": True,
                "is_superuser": False
            },
            {
                "email": "student@ignite.com",
                "name": "Koffi",
                "role": "student",
                "is_staff": False,
                "is_superuser": False
            },
        ],

        # User creation
        for data in users_data:
            if not User.objects.filter(email=data['email']).exists():
                user = User.objects.create_user(
                    email=data["email"],
                    password="password123",
                    name=data["name"],
                    is_staff=data["is_staff"],
                    is_superuser=data['is_superuser']
                )
                # On ajoute le role
                user.roles.add(role_objs[data['role']])
                self.stdout.write(self.style.SUCCESS(f"User created: {data['email']} [{data['role']}]"))
            else:
                self.stdout.write(self.style.WARNING(f"User {data['email']} already created."))


