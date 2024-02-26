from rest_framework import serializers
from .models import Category, Author, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name']

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    categoriesSubmit = serializers.ListField(child=serializers.CharField(), write_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categoriesSubmit', 'categories', 'published_date']

    def create(self, validated_data):
        author_name = validated_data.pop('author')
        categories_names = validated_data.pop('categoriesSubmit')

        author, _ = Author.objects.get_or_create(name=author_name)
        book = Book.objects.create(author=author, **validated_data)

        for category_name in categories_names:
            category, _ = Category.objects.get_or_create(name=category_name)
            book.categories.add(category)

        return book

    def update(self, instance, validated_data):
        if 'author' in validated_data:
            author_name = validated_data.pop('author')
            author, _ = Author.objects.get_or_create(name=author_name)
            instance.author = author

        if 'categoriesSubmit' in validated_data:
            categories_names = validated_data.pop('categoriesSubmit')
            # Clear existing categories and add the new ones
            instance.categories.clear()
            for category_name in categories_names:
                category, _ = Category.objects.get_or_create(name=category_name)
                instance.categories.add(category)

        # Update any other fields if necessary
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance