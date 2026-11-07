from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MushaerehRoomViewSet

router = DefaultRouter()
router.register(r'rooms', MushaerehRoomViewSet, basename='mushaereh-room')

urlpatterns = [
    path('', include(router.urls)),
]
