from django.core.management.base import BaseCommand
from subcategories.models import SubCategory
from categories.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Seeds subcategories for the existing 10 main categories"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL("--- STARTING SUBCATEGORIES SEEDING ---"))

        # Dictionnaire associant les catégories existantes à leurs nouvelles sous-catégories
        data = {
            "Web Development": ["Frontend React", "Backend Python Django", "Fullstack Next.js", "API Architecture", "Web3 & Blockchain"],
            "Artificial Intelligence": ["Machine Learning", "Deep Learning", "Prompt Engineering", "Natural Language Processing", "Computer Vision"],
            "Data Science": ["Python Data Analysis", "Business Intelligence", "Big Data Engineering", "Data Visualization", "Statistical Modeling"],
            "Cloud & DevOps": ["AWS Cloud Solutions", "Docker & Kubernetes", "Terraform & IaC", "Microsoft Azure", "CI/CD Pipelines"],
            "Cybersecurity": ["Ethical Hacking", "Network Security", "Malware Analysis", "Cryptography", "Security Auditing"],
            "Design & Creative": ["UI Design", "UX Research", "Design Thinking", "Figma Mastering", "Motion Design"],
            "Digital Marketing": ["SEO Optimization", "Social Media Marketing", "Growth Hacking", "Email Automation", "Performance Marketing"],
            "Business & Finance": ["Agile Project Management", "Business Strategy", "Fintech Solutions", "E-commerce Management", "Venture Capital & Pitching"],
            "Soft Skills": ["Leadership & Strategy", "Time Management", "Effective Communication", "Negotiation Skills", "Emotional Intelligence"],
            "Mobile Development": ["Flutter & Dart", "React Native", "iOS Swift Development", "Android Kotlin", "Mobile UX Design"],
        }

        for cat_name, sub_list in data.items():
            try:
                # On récupère la catégorie parente (doit exister)
                category = Category.objects.get(name=cat_name)

                for sub_name in sub_list:
                    # Création de la sous-catégorie
                    sub_obj, created = SubCategory.objects.get_or_create(
                        category=category,
                        name=sub_name,
                        defaults={'slug': slugify(sub_name)}
                    )

                    if created:
                        self.stdout.write(f"   ✅ Created: '{sub_name}' inside '{cat_name}'")
                    else:
                        self.stdout.write(f"   🆗 Already exists: '{sub_name}'")

            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"   ❌ Category '{cat_name}' not found! Please seed categories first."))

        self.stdout.write(self.style.SUCCESS("--- SUBCATEGORIES SEEDING COMPLETE ---"))

