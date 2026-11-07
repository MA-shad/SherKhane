from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PoetViewSet, PoemViewSet, VerseViewSet, RhythmViewSet

router = DefaultRouter()
router.register(r'poets', PoetViewSet, basename='poet')
router.register(r'poems', PoemViewSet, basename='poem')
router.register(r'verses', VerseViewSet, basename='verse')
router.register(r'rhythms', RhythmViewSet, basename='rhythm')

urlpatterns = [
    path('', include(router.urls)),
]
