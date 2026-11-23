from django.urls import path
from .views import StartMoshaerehView, PlayMoshaerehTurnView, MoshaerehDetailView

app_name = 'games'

urlpatterns = [
    path('moshaereh/start/', StartMoshaerehView.as_view(), name='moshaereh-start'),
    path('moshaereh/<int:session_id>/play/', PlayMoshaerehTurnView.as_view(), name='moshaereh-play'),
    path('moshaereh/<int:session_id>/', MoshaerehDetailView.as_view(), name='moshaereh-detail'),
]