from django.db import models


# Метод для определения пути загрузки файлов
def upload_to(instance, filename):
    # Формируем путь сохранения файла вида 'books/<book_id>/<filename>'
    return f'books/{instance.book.id}/{filename}'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    files = models.ManyToManyField('BookFile')

    def __str__(self):
        return self.title


class BookFile(models.Model):
    FILE_CHOICES = (
        ('pdf', 'PDF'),
        ('txt', 'TXT'),
        ('epub', 'EPUB'),
        ('doc', 'DOC'),
        # Добавьте другие форматы файлов по мере необходимости
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to)
    file_format = models.CharField(max_length=4, choices=FILE_CHOICES)

    def __str__(self):
        return f"{self.book.title} - {self.file_format}"
