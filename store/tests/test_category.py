import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from store.models import Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_admin_user(db):
    return User.objects.create_user(username='admin', password='password', is_staff=True)

@pytest.fixture
def create_category(db):
    return Category.objects.create(name='Fiction')

@pytest.mark.django_db
def test_category_create(api_client, create_admin_user):
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.post('/store/category/', {'name': 'Fiction'})  # Updated URL
    assert response.status_code == 201
    assert Category.objects.count() == 1
    assert Category.objects.get().name == 'Fiction'

@pytest.mark.django_db
def test_category_list(api_client, create_category):
    response = api_client.get('/store/category/')  # Updated URL
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Fiction'

@pytest.mark.django_db
def test_category_update(api_client, create_admin_user, create_category):
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.patch(f'/store/category/{create_category.id}/', {'name': 'Non-Fiction'})  # Updated URL
    assert response.status_code == 200
    assert Category.objects.get().name == 'Non-Fiction'

@pytest.mark.django_db
def test_category_delete_permission(api_client, create_admin_user, create_category):
    # Test delete by non-admin user
    non_admin_user = User.objects.create_user(username='user', password='password')
    api_client.force_authenticate(user=non_admin_user)
    response = api_client.delete(f'/store/category/{create_category.id}/')  # Updated URL for non-admin
    assert response.status_code == 403  # Permission denied

    # Test delete by admin user
    api_client.force_authenticate(user=create_admin_user)
    response = api_client.delete(f'/store/category/{create_category.id}/')  # Updated URL for admin
    assert response.status_code == 204
    assert Category.objects.count() == 0