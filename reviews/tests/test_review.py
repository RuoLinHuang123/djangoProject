import pytest
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from reviews.models import Review

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username='admin', is_staff=True)

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username='user')

@pytest.fixture
def content_type(db):
    return ContentType.objects.create(model='testmodel', app_label='testapp')

@pytest.fixture
def review(db, regular_user, content_type):
    return Review.objects.create(
        user=regular_user, 
        content_type=content_type, 
        object_id=1, 
        text='Sample review'
    )

@pytest.fixture
def client():
    return APIClient()

def test_get_all_reviews(client, review):
    response = client.get('/reviews/review/') 
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_filter_reviews_by_user_id(client, review, regular_user):
    response = client.get(f'/reviews/review/?user_id={regular_user.id}')
    assert response.status_code == 200
    assert len(response.json()) == 1
    print(response.json()[0])
    assert response.json()[0]['user_id'] == regular_user.id

def test_filter_reviews_by_user_id2(client, review, regular_user):
    response = client.get(f'/reviews/review/?user_id={regular_user.id+1}')
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_delete_review_by_admin(client, admin_user, review):
    client.force_authenticate(user=admin_user)
    response = client.delete(f'/reviews/review/{review.id}/')
    assert response.status_code == 204

def test_delete_review_by_non_admin(client, regular_user, review):
    client.force_authenticate(user=regular_user)
    response = client.delete(f'/reviews/review/{review.id}/')
    assert response.status_code == 403 
