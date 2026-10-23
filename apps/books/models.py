from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название библиотеки')
    address = models.CharField(max_length=255, verbose_name='Адрес библиотеки')
    city = models.CharField(max_length=100, verbose_name='Город')

    class Meta:
        verbose_name = 'Библиотека'
        verbose_name_plural = 'Библиотеки'

    def __str__(self):
        return f"{self.name} ({self.city})"


class Books(models.Model):
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name='books',
        null=True,
        blank=True,
        verbose_name='Библиотека'
    )
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.CharField(max_length=255, verbose_name='Автор')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
