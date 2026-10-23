from django.urls import path
from .views import TaskView, TaskDetailView, TaskGroupedView

urlpatterns = [
    path('', TaskView.as_view(), name='task-list'),
    path('grouped/', TaskGroupedView.as_view(), name='task-grouped'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
