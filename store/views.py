from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Category, Author, Book
from .serializer import CategorySerializer, AuthorSerializer, BookSerializer
from .permission import IsAdmin

# Create your views here.
class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorViewSet(ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Book.objects.select_related('author').prefetch_related('categories').all()
    serializer_class = BookSerializer


   


    

