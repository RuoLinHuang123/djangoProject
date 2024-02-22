from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('category',views.CategoryViewSet)
router.register('author',views.AuthorViewSet)
router.register('book',views.BookViewSet)

urlpatterns = router.urls