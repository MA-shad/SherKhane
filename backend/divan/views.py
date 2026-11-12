from rest_framework import viewsets
from .models import Poet, Work, Rhythm, Poem, Verse
from .serializers import (
    PoetSerializer,
    WorkSerializer,
    RhythmSerializer,
    VerseSerializer,
    PoemListSerializer,
    PoemDetailSerializer,
)
from rest_framework import filters
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class PoetViewSet(viewsets.ModelViewSet):
    queryset = Poet.objects.prefetch_related('works').all().order_by('name')
    serializer_class = PoetSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'century']
    permission_classes = [IsAdminOrReadOnly]


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.select_related('poet').all()
    serializer_class = WorkSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'poet__name']
    ordering_fields = ['title']
    permission_classes = [IsAdminOrReadOnly]


class RhythmViewSet(viewsets.ModelViewSet):
    queryset = Rhythm.objects.all()
    serializer_class = RhythmSerializer
    permission_classes = [IsAdminOrReadOnly]


class PoemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'poet__name']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PoemListSerializer
        return PoemDetailSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Poem.objects.select_related('poet', 'work', 'rhythm').all()
        return Poem.objects.select_related('poet', 'work', 'rhythm').prefetch_related('verses').all()


class VerseViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.select_related('poem').all()
    serializer_class = VerseSerializer
    permission_classes = [IsAdminOrReadOnly]


