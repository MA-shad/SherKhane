from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DailyContentViewSet

router = DefaultRouter()
router.register(r'culture', DailyContentViewSet, basename='daily-content')

urlpatterns = [
    path('', include(router.urls)),
]
