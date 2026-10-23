from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Books, Library
from .serializers import BooksSerializer, LibrarySerializer

BOOKS_TAG = ['Книги и Библиотеки (Books)']


class BookListApi(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BooksSerializer

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Список всех книг',
        responses={200: BooksSerializer(many=True)},
    )
    def get(self, request):
        books = Books.objects.select_related('library').all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Добавить новую книгу',
        request=BooksSerializer,
        responses={201: BooksSerializer},
    )
    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailApi(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BooksSerializer

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Детали книги по ID',
        responses={200: BooksSerializer},
    )
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BooksSerializer(book)
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Полное обновление книги (PUT)',
        request=BooksSerializer,
        responses={200: BooksSerializer},
    )
    def put(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BooksSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Частичное обновление книги (PATCH)',
        request=BooksSerializer,
        responses={200: BooksSerializer},
    )
    def patch(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        serializer = BooksSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Удаление книги (DELETE)',
        responses={204: OpenApiResponse(description='Книга успешно удалена')},
    )
    def delete(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LibraryListApi(APIView):
    """
    Получение списка библиотек со списком принадлежащих им книг (вложенный сериализатор),
    а также создание новой библиотеки.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LibrarySerializer

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Список библиотек с вложенными книгами',
        responses={200: LibrarySerializer(many=True)},
    )
    def get(self, request):
        libraries = Library.objects.prefetch_related('books').all()
        serializer = LibrarySerializer(libraries, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Создать новую библиотеку',
        request=LibrarySerializer,
        responses={201: LibrarySerializer},
    )
    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LibraryDetailApi(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LibrarySerializer

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Детали библиотеки по ID',
        responses={200: LibrarySerializer},
    )
    def get(self, request, pk):
        library = get_object_or_404(Library.objects.prefetch_related('books'), pk=pk)
        serializer = LibrarySerializer(library)
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Полное обновление библиотеки (PUT)',
        request=LibrarySerializer,
        responses={200: LibrarySerializer},
    )
    def put(self, request, pk):
        library = get_object_or_404(Library, pk=pk)
        serializer = LibrarySerializer(library, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Частичное обновление библиотеки (PATCH)',
        request=LibrarySerializer,
        responses={200: LibrarySerializer},
    )
    def patch(self, request, pk):
        library = get_object_or_404(Library, pk=pk)
        serializer = LibrarySerializer(library, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=BOOKS_TAG,
        summary='Удаление библиотеки (DELETE)',
        responses={204: OpenApiResponse(description='Библиотека удалена')},
    )
    def delete(self, request, pk):
        library = get_object_or_404(Library, pk=pk)
        library.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
