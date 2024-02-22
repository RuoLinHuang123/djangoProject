from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields like biography, birthdate, etc. as needed
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    published_date = models.DateField()
    # Add other fields as needed
    def __str__(self):
        return self.title

