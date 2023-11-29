from django.core.management import call_command
from django.http import HttpResponse, JsonResponse
from haystack.management.commands import update_index, rebuild_index
from haystack.query import SearchQuerySet
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


@api_view(['POST'])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        rebuild_index.Command().handle(interactive=False, remove=True, verbosity=2)
        return Response("Book added and indexed successfully!", status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_book(request):
    query = request.GET.get('q', '')
    search_results = perform_base_search(query)
    if query:
        serialized_results = [
            {
                'title': result.title,
                'author': result.author,
                'description': result.description,
                'image_url': result.image_url,
            }
            for result in search_results
        ]
        return JsonResponse({'results': serialized_results})
    else:
        return JsonResponse({'message': 'No search query provided'}, status=400)


def perform_base_search(query):
    return SearchQuerySet().filter(text=query)


class HomeView(generics.RetrieveAPIView):
    def index(self):
        return HttpResponse("Weclome")
