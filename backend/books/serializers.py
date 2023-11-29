from rest_framework import serializers
from .models import Book, BookFile


class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFile
        read_only_fields = ('file', 'file_format')


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
