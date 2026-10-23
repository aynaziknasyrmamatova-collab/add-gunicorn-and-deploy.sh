from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )
    title = models.CharField(max_length=60, verbose_name='Заголовок')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Дедлайн')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
