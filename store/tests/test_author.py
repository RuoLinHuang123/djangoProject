import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Author

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_admin_user(db):
    return User.objects.create_user(username='admin', password='password', is_staff=True)

@pytest.fixture
def create_author(db):
    return Author.objects.create(name='J.K. Rowling')

@pytest.mark.django_db
def test_author_create(api_client, create_admin_user):
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.post('/store/author/', {'name': 'George R.R. Martin'})
    assert response.status_code == 201
    assert Author.objects.count() == 1
    assert Author.objects.get().name == 'George R.R. Martin'

@pytest.mark.django_db
def test_author_list(api_client, create_author):
    response = api_client.get('/store/author/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'J.K. Rowling'

@pytest.mark.django_db
def test_author_update(api_client, create_admin_user, create_author):
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.patch(f'/store/author/{create_author.id}/', {'name': 'Robert Jordan'})
    assert response.status_code == 200
    assert Author.objects.get().name == 'Robert Jordan'

@pytest.mark.django_db
def test_author_delete_permission(api_client, create_admin_user, create_author):
    # Test delete by non-admin user
    non_admin_user = User.objects.create_user(username='user', password='password')
    api_client.force_authenticate(user=non_admin_user)
    response = api_client.delete(f'/store/author/{create_author.id}/')
    assert response.status_code == 403  # Permission denied

    # Test delete by admin user
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.delete(f'/store/author/{create_author.id}/')
    assert response.status_code == 204
    assert Author.objects.count() == 0