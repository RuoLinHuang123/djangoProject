from django.contrib import admin
from django.db.models import Count
from .models import Category, Author, Book

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')

    def get_queryset(self, request):
        # Annotate each author with the count of books
        queryset = super().get_queryset(request).annotate(book_count=Count('book'))
        return queryset

    @admin.display(ordering='book_count')
    def book_count(self, obj):
        # Access the annotated book count
        return obj.book_count

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')

    def get_queryset(self, request):
        # Annotate each author with the count of books
        queryset = super().get_queryset(request).annotate(book_count=Count('book'))
        return queryset

    @admin.display(ordering='book_count')
    def book_count(self, obj):
        # Access the annotated book count
        return obj.book_count

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')  # Customize as needed
    list_filter = ('author',  'published_date')  # Add filters
    filter_horizontal = ('categories',)
    search_fields = ('title', 'author__name')  # Enable search by title and author name