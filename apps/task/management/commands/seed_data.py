from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.task.models import Task


class Command(BaseCommand):
    help = "Создает тестовых пользователей и задачи для демонстрации темы Урока 2"

    def handle(self, *args, **options):
        self.stdout.write("Создание тестовых данных...")

        user1, _ = User.objects.get_or_create(username="alice", defaults={"email": "alice@example.com", "first_name": "Алиса"})
        user2, _ = User.objects.get_or_create(username="bob", defaults={"email": "bob@example.com", "first_name": "Боб"})

        tasks_data = [
            {"title": "Изучить ModelSerializer", "description": "Понять как работают вложенные сериализаторы и поля", "user": user1, "completed": True},
            {"title": "Разобраться с проблемой N+1", "description": "Использовать select_related для оптимизации SQL", "user": user1, "completed": False},
            {"title": "Настроить LocMem кэширование", "description": "Использовать cache.get и cache.set в APIView", "user": user2, "completed": False},
            {"title": "Реализовать валидацию данных", "description": "Написать validate_title и validate методы", "user": user2, "completed": True},
            {"title": "Протестировать бенчмарк эндпоинт", "description": "Открыть /task/benchmark/ и сравнить скорость", "user": user1, "completed": False},
        ]

        created_count = 0
        for data in tasks_data:
            _, created = Task.objects.get_or_create(title=data["title"], defaults=data)
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Успешно! Добавлено {created_count} новых задач. Всего в базе: {Task.objects.count()} задач."))
