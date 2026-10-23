from django.utils import timezone
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "user",
            "deadline",
            "is_completed",
            "time_left",
        )
        read_only_fields = ("id", "user", "time_left")

    def get_time_left(self, obj) -> str:
        if not obj.deadline:
            return "Дедлайн не указан"

        now = timezone.now()
        if now > obj.deadline:
            return "Дедлайн просрочен"

        diff = obj.deadline - now
        total_seconds = int(diff.total_seconds())
        days = diff.days
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if days > 1:
            return f"{days} days left"
        elif days == 1:
            return "1 day left"
        elif hours > 1:
            return f"{hours} hours left"
        elif hours == 1:
            return "1 hour left"
        elif minutes > 1:
            return f"{minutes} minutes left"
        else:
            return "Менее минуты осталось"

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Минимум 3 символа в названии!")
        return value.strip()
