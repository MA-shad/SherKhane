# from django.db.models.aggregates import Count
# from django.shortcuts import render

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
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer


class VerseViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer

# from rest_framework import viewsets
# from .models import Poet, Poem, Verse
# from .serializers import PoetSerializer, PoemSerializer, VerseSerializer
#
#
# class PoetViewSet(viewsets.ModelViewSet):
#     queryset = Poet.objects.annotate(poems_count=Count('poems').order_by('name'))
#     serializer_class = PoetSerializer
#
#
# class PoemViewSet(viewsets.ModelViewSet):
#     queryset = Poem.objects.select_related('poet').prefetch_related('verse').all
#     serializer_class = PoemSerializer
#
#
# class VerseViewSet(viewsets.ModelViewSet):
#     queryset = Verse.objects.select_related('poem').all()
#     serializer_class = VerseSerializer