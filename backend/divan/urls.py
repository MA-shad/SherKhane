from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PoetViewSet, PoemViewSet, VerseViewSet

router = DefaultRouter()

router.register(r'poets', PoetViewSet, basename='poet')
router.register(r'poems', PoemViewSet, basename='poem')
router.register(r'verses', VerseViewSet, basename='verse')

urlpatterns = [
    path('', include(router.urls)),
]
