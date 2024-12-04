import random
from faker import Faker
from django.core.management.base import BaseCommand
from blog.models import Blog, BlogCategory
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake data for Blog API'

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Create a fake user
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'
        )
        # Create random categories
        categories = []
        for _ in range(5):
            category = BlogCategory.objects.create(
                user=user,
                name=fake.word()
            )
            categories.append(category)
        # Generate fake blogs
        for _ in range(20):
            Blog.objects.create(
                user=user,
                category=random.choice(categories),
                title=fake.sentence(nb_words=6),
                slug=fake.slug(),
                summary=fake.sentence(nb_words=10),
                description=fake.paragraph(nb_sentences=5),
                photo=fake.image_url(),  # Optional: Add image generation logic if needed
                status=random.choice([0, 1]),  # Example: 0 = Draft, 1 = Published
                created_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year()
            )

        self.stdout.write(self.style.SUCCESS("Fake data successfully created!"))
