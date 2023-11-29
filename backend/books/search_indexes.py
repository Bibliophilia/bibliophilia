from .models import Book
from haystack import indexes


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name="search/book_text.txt")
    title = indexes.CharField(model_attr='title')
    author = indexes.CharField(model_attr='author')
    description = indexes.CharField(model_attr='description')
    image = indexes.LocationField(model_attr='image_url')

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
