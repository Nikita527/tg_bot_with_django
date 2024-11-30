import os

from dotenv import load_dotenv

from django.core.management import BaseCommand

from users.models import User

load_dotenv()


class Command(BaseCommand):
    """Команда для создания суперпользователя."""

    def handle(self, *args, **options):
        """Создание суперпользователя."""
        username = os.getenv("SU_USERNAME")
        telegram_id = int(os.getenv("SU_TELEGRAM_ID"))
        password = os.getenv("SU_PASSWORD")
        first_name = os.getenv("SU_FIRST_NAME", "")
        last_name = os.getenv("SU_LAST_NAME", "")

        admin = User.objects.create_superuser(
            username=username,
            telegram_id=telegram_id,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        admin.save()
