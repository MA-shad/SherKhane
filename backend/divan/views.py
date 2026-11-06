from rest_framework import viewsets
from .models import Poet, Rhythm, Poem, Verse
from .serializers import PoetSerializer, RhythmSerializer, PoemSerializer, VerseSerializer


class PoetViewSet(viewsets.ModelViewSet):
    queryset = Poet.objects.all().order_by('name')
    serializer_class = PoetSerializer


class RhythmViewSet(viewsets.ModelViewSet):
    queryset = Rhythm.objects.all()
    serializer_class = RhythmSerializer


class PoemViewSet(viewsets.ModelViewSet):
    queryset = Poem.objects.select_related('poet', 'rhythm').prefetch_related('verses').all()
    serializer_class = PoemSerializer


class VerseViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.select_related('poem').all()
    serializer_class = VerseSerializer
