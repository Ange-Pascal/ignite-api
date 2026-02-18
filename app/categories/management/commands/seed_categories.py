from django.core.management.base import BaseCommand
from django.utils.text import slugify
from categories.models import Category  # Remplace par ton chemin exact

class Command(BaseCommand):
    help = "Seeds the database with professional English category names"

    def handle(self, *args, **options):
        # Liste généraliste pour tout type de LMS
        category_names = [
            "Web Development",
            "Artificial Intelligence",
            "Data Science",
            "Cloud & DevOps",
            "Cybersecurity",
            "Design & Creative",
            "Digital Marketing",
            "Business & Finance",
            "Soft Skills",
            "Mobile Development"
        ]

       # Remplace la ligne 22 par :
        self.stdout.write(self.style.HTTP_INFO("--- SEEDING CATEGORIES ---"))

        for name in category_names:
            slug = slugify(name)
            obj, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {name}"))
            else:
                self.stdout.write(f"🟡 Already exists: {name}")

        self.stdout.write(self.style.SUCCESS("--- CATEGORIES SEEDING COMPLETE ---"))
