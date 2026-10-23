from collections import defaultdict
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly

TASK_TAG = ['Задачи (Tasks)']


def get_grouped_tasks_data():
    """Группировка задач по дате дедлайна"""
    tasks = Task.objects.select_related('user').all()
    grouped = defaultdict(list)
    for task in tasks:
        task_data = TaskSerializer(task).data
        if task.deadline:
            date_key = task.deadline.strftime("%Y-%m-%d")
        else:
            date_key = "no_deadline"
        grouped[date_key].append(task_data)
    return dict(grouped)


def clear_task_caches():
    """Сброс кэша для списка задач и группировки"""
    cache.delete("tasks")
    cache.delete("tasks_grouped")


class TaskView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer

    @extend_schema(
        tags=TASK_TAG,
        summary='Список задач (кэш на 5 мин / группировка через ?group_by=date)',
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request):
        group_by = request.query_params.get("group_by")
        if group_by == "date":
            cached_grouped = cache.get("tasks_grouped")
            if cached_grouped is not None:
                return Response(cached_grouped)
            grouped_data = get_grouped_tasks_data()
            cache.set("tasks_grouped", grouped_data, timeout=300)
            return Response(grouped_data)

        tasks_data = cache.get("tasks")
        if tasks_data is None:
            tasks = Task.objects.select_related('user').all()
            serializer = TaskSerializer(tasks, many=True)
            tasks_data = serializer.data
            cache.set("tasks", tasks_data, timeout=300)

        return Response(tasks_data)

    @extend_schema(
        tags=TASK_TAG,
        summary='Создание новой задачи',
        request=TaskSerializer,
        responses={201: TaskSerializer},
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user if request.user.is_authenticated else None
        serializer.save(user=user)
        clear_task_caches()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskGroupedView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer

    @extend_schema(
        tags=TASK_TAG,
        summary='Группировка задач по дате дедлайна (/task/grouped/)',
        responses={200: OpenApiResponse(description='Словарь задач с ключами-датами')},
    )
    def get(self, request):
        cached_grouped = cache.get("tasks_grouped")
        if cached_grouped is not None:
            return Response(cached_grouped)

        grouped_data = get_grouped_tasks_data()
        cache.set("tasks_grouped", grouped_data, timeout=300)
        return Response(grouped_data)


class TaskDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskSerializer

    def get_object(self, pk):
        task = get_object_or_404(Task.objects.select_related('user'), pk=pk)
        self.check_object_permissions(self.request, task)
        return task

    @extend_schema(
        tags=TASK_TAG,
        summary='Детали задачи по ID',
        responses={200: TaskSerializer},
    )
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @extend_schema(
        tags=TASK_TAG,
        summary='Полное обновление задачи (PUT)',
        request=TaskSerializer,
        responses={200: TaskSerializer},
    )
    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        clear_task_caches()
        return Response(serializer.data)

    @extend_schema(
        tags=TASK_TAG,
        summary='Частичное обновление задачи (PATCH)',
        request=TaskSerializer,
        responses={200: TaskSerializer},
    )
    def patch(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        clear_task_caches()
        return Response(serializer.data)

    @extend_schema(
        tags=TASK_TAG,
        summary='Удаление задачи (DELETE)',
        responses={204: OpenApiResponse(description='Задача удалена')},
    )
    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        clear_task_caches()
        return Response(status=status.HTTP_204_NO_CONTENT)
