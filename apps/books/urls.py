from django.urls import path
from .views import (
    BookListApi,
    BookDetailApi,
    LibraryListApi,
    LibraryDetailApi,
)

urlpatterns = [
    path('books/', BookListApi.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailApi.as_view(), name='book-detail'),
    path('libraries/', LibraryListApi.as_view(), name='library-list'),
    path('libraries/<int:pk>/', LibraryDetailApi.as_view(), name='library-detail'),
]
