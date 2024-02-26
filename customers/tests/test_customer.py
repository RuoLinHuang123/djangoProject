import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from customers.models import Customer

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def create_customer(db):
    def make_customer(user, **kwargs):
        return Customer.objects.create(user=user, **kwargs)
    return make_customer

def test_customer_me_not_authenticated(api_client):
    response = api_client.get('/your-url-path/me/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_customer_me_not_found(api_client, create_user):
    user = create_user(username='user1', password='bar')
    api_client.force_authenticate(user=user)
    response = api_client.get('/customers/customer/me/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_customer_me_get_success(api_client, create_user, create_customer):
    user = create_user(username='user2', email='user2@example.com', password='bar')
    customer = create_customer(user=user, first_name='John', last_name='Doe', email='user2@example.com',phone='123456')
    api_client.force_authenticate(user=user)
    response = api_client.get('/customers/customer/me/')
    assert response.status_code == status.HTTP_200_OK
    print(response.data)
    assert response.data == {
        'id': customer.id,
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'user2@example.com',
        'phone': '123456',
        # 'password' field is write-only, it should not be returned in the response
    }

@pytest.mark.django_db
def test_customer_me_put_success(api_client, create_user, create_customer):
    user = create_user(username='user3', email='user3@example.com', password='bar')
    customer = create_customer(user=user, first_name='Jane', last_name='Doe', email='user3@example.com')
    api_client.force_authenticate(user=user)
    updated_data = {'first_name': 'Jane Updated', 'last_name': 'Doe Updated'}
    response = api_client.put('/customers/customer/me/', updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'Jane Updated'
    assert response.data['last_name'] == 'Doe Updated'

@pytest.mark.django_db
def test_create_customer_success(api_client):
    customer_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'johndoe@example.com',
        'phone': '1234567890',
        'password': 'newpassword'
    }
    response = api_client.post('/customers/customer/', customer_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data

@pytest.mark.django_db
def test_get_customer_list_success(api_client, create_user, create_customer):
    user = create_user(username='user1', email='user1@example.com', password='password')
    create_customer(user=user, first_name='John', last_name='Doe', email='user1@example.com')
    response = api_client.get('/customers/customer/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1  # Assuming there's at least one customer in the list

@pytest.mark.django_db
def test_update_customer_success(api_client, create_user, create_customer):
    user = create_user(username='user2', email='user2@example.com', password='password', is_staff=True)
    customer = create_customer(user=user, first_name='Jane', last_name='Doe', email='user2@example.com')
    api_client.force_authenticate(user=user)
    updated_data = {'first_name': 'Jane Updated', 'last_name': 'Doe Updated'}
    response = api_client.patch(f'/customers/customer/{customer.id}/', updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'Jane Updated'
    assert response.data['last_name'] == 'Doe Updated'

@pytest.mark.django_db
def test_delete_customer_success(api_client, create_user, create_customer):
    user = create_user(username='user3', email='user3@example.com', password='password', is_staff=True)
    customer = create_customer(user=user, first_name='Jane', last_name='Doe', email='user3@example.com')
    api_client.force_authenticate(user=user)
    response = api_client.delete(f'/customers/customer/{customer.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

