from django.contrib import admin
from .models import Books, Library


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'city')
    search_fields = ('name', 'address', 'city')
    list_filter = ('city',)


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price', 'library')
    search_fields = ('title', 'author')
    list_filter = ('library', 'author')
