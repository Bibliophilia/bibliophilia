from django.db import models


# Метод для определения пути загрузки файлов
def upload_image_to(instance, filename):
    filename = f"{instance.book.id}.{filename.split('.')[-1]}"
    return f'public/book-images/{instance.book.id}/{filename}'


def upload_file_to(instance, filename):
    filename = f"{instance.book.id}.{filename.split('.')[-1]}"
    return f'private/book-files/{instance.book.id}/{filename}'


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to=upload_image_to)
    files = models.ManyToManyField('BookFile', related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'books'


class BookFile(models.Model):
    FILE_CHOICES = (
        ('pdf', 'PDF'),
        ('txt', 'TXT'),
        ('epub', 'EPUB'),
        ('doc', 'DOC'),
        # Добавьте другие форматы файлов по мере необходимости
    )
    book = models.ForeignKey(Book, related_name='book_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_file_to)
    file_format = models.CharField(max_length=4, choices=FILE_CHOICES)

    class Meta:
        app_label = 'books'

    def __str__(self):
        return f"{self.book.title} - {self.file_format}"
