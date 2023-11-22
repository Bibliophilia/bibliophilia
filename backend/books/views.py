from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from .usecases import save_book, perform_search, get_book_info


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serialized_data = serializer.validated_data
            result = save_book(serialized_data)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            data = {"result": "Invalid data"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        result = perform_search(query=query)
        return Response(result, status=status.HTTP_200_OK)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        id = request.GET.get(pk=pk)
        result = get_book_info(id)
        return Response(result, status=status.HTTP_200_OK)


class HomeView(generics.RetrieveAPIView):

    def index(self):
        return HttpResponse("Weclome")
