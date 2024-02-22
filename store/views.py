from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Author, Book
from .serializer import CategorySerializer, AuthorSerializer, BookSerializer

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('author').prefetch_related('categories').all()
    serializer_class = BookSerializer


   


    

