from rest_framework import serializers
from .models import Book, BookFile


class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFile
        read_only_fields = ('file', 'file_format')


class BookSerializer(serializers.ModelSerializer):
    files = BookFileSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        read_only_fields = ('id', 'title', 'author', 'description', 'image', 'files')
