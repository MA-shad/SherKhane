from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Poet, Poem, Verse
from .serializers import PoetSerializer, PoemSerializer, VerseSerializer


class PoetViewSet(viewsets.ModelViewSet):
    queryset = Poet.objects.all()
    serializer_class = PoetSerializer


class PoemViewSet(viewsets.ModelViewSet):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer


class VerseViewSet(viewsets.ModelViewSet):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer