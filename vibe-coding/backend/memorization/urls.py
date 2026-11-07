from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemorizationViewSet

router = DefaultRouter()
router.register(r'studio', MemorizationViewSet, basename='memorization')

urlpatterns = [
    path('', include(router.urls)),
]
