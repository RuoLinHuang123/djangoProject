import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Author, Category, Book

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_admin_user(db):
    return User.objects.create_user(username='admin', password='password', is_staff=True)

@pytest.fixture
def create_author(db):
    author = Author.objects.create(name='J.R.R. Tolkien')
    return author

@pytest.fixture
def create_category(db):
    category = Category.objects.create(name='Fantasy')
    return category

@pytest.fixture
def create_book(db, create_author, create_category):
    book = Book.objects.create(title='The Hobbit', author=create_author, published_date='1937-09-21')
    book.categories.add(create_category)
    return book

@pytest.mark.django_db
def test_book_create(api_client, create_admin_user):
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.post('/store/book/', {
        'title': 'The Lord of the Rings',
        'author': 'J.R.R. Tolkien',
        'categoriesSubmit': ['Fantasy'],
        'published_date': '1954-07-29'
    })
    assert response.status_code == 201
    assert Book.objects.count() == 1
    book = Book.objects.get()
    assert book.title == 'The Lord of the Rings'
    assert book.author.name == 'J.R.R. Tolkien'
    assert book.categories.count() == 1
    assert book.categories.first().name == 'Fantasy'

@pytest.mark.django_db
def test_book_list(api_client, create_book):
    response = api_client.get('/store/book/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'The Hobbit'

@pytest.mark.django_db
def test_book_update(api_client, create_admin_user, create_book):
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.patch(f'/store/book/{create_book.id}/', {
        'title': 'The Silmarillion',
        'categoriesSubmit': ['High Fantasy']
    })
    assert response.status_code == 200
    updated_book = Book.objects.get(id=create_book.id)
    assert updated_book.title == 'The Silmarillion'
    assert updated_book.categories.count() == 1
    assert updated_book.categories.first().name == 'High Fantasy'

@pytest.mark.django_db
def test_book_delete_permission(api_client, create_admin_user, create_book):
    # Test delete by non-admin user
    non_admin_user = User.objects.create_user(username='user', password='password')
    api_client.force_authenticate(user=non_admin_user)
    response = api_client.delete(f'/store/book/{create_book.id}/')
    assert response.status_code == 403  # Permission denied

    # Test delete by admin user
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.delete(f'/store/book/{create_book.id}/')
    assert response.status_code == 204
    assert Book.objects.count() == 0