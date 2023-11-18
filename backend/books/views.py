from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')  # Получаем запрос из параметров запроса
        page_number = self.request.query_params.get('page', '')
        # TODO: передавать нужное число книг
        return Book.objects.filter(title__icontains=query)  # Фильтруем книги по названию


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
