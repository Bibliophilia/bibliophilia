from django.db import models


# Метод для определения пути загрузки файлов
def upload_image_to(instance, filename):
    filename = f"{instance.id}.{filename.split('.')[-1]}"
    return f'public/book-images/{instance.id}/{filename}'


def upload_file_to(instance, filename):
    filename = f"{instance.id}.{filename.split('.')[-1]}"
    return f'private/files/books/{instance.id}/{filename}'


class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        app_label = 'books'


class BookFile(models.Model):
    FILE_CHOICES = (
        ('pdf', 'PDF'),
        ('txt', 'TXT'),
        ('epub', 'EPUB'),
        ('doc', 'DOC'),
        # Добавьте другие форматы файлов по мере необходимости
    )
    file = models.FileField(upload_to=upload_file_to)
    file_format = models.CharField(max_length=4, choices=FILE_CHOICES)

    class Meta:
        managed = False


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    image = models.FileField(upload_to=upload_image_to)

    def image_url(self):
        if self.image:
            return self.image.url
        return None

    class Meta:
        db_table = 'books'

    def __unicode__(self):
        return "{}:{}".format(self.title, self.author)
    # files = models.ManyToManyField(BookFile, related_name='book', on_delete=models.CASCADE)
