import random
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Q
from core.normalizer import normalize_persian_text
from .models import Poet, Rhythm, Work, Poem, Verse
from .serializers import (
    PoetListSerializer,
    PoetDetailSerializer,
    WorkSerializer,
    PoemListSerializer,
    PoemDetailSerializer,
    VerseSerializer,
    RhythmSerializer
)


class PoetViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        return Poet.objects.annotate(poems_count=Count('poems')).order_by('century', 'name')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PoetDetailSerializer
        return PoetListSerializer


class PoemViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        queryset = Poem.objects.select_related('poet', 'rhythm', 'work').prefetch_related('verses').annotate(verses_count=Count('verses'))

        # Search parameter with Persian text normalization
        search_query = self.request.query_params.get('search', '').strip()
        if search_query:
            norm_query = normalize_persian_text(search_query)
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(verses__normalized_text__icontains=norm_query) |
                Q(poet__name__icontains=search_query)
            ).distinct()

        # Poet filter (by id or slug)
        poet_param = self.request.query_params.get('poet')
        if poet_param:
            if poet_param.isdigit():
                queryset = queryset.filter(poet_id=int(poet_param))
            else:
                queryset = queryset.filter(poet__slug=poet_param)

        # Poem Type filter
        poem_type = self.request.query_params.get('poem_type')
        if poem_type:
            queryset = queryset.filter(poem_type=poem_type)

        # Century filter
        century = self.request.query_params.get('century')
        if century and century.isdigit():
            queryset = queryset.filter(poet__century=int(century))

        return queryset.order_by('poet__century', 'order_in_work', 'id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PoemDetailSerializer
        return PoemListSerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        """Return a random complete poem for reading and inspiration"""
        pks = list(Poem.objects.values_list('pk', flat=True))
        if not pks:
            return Response({'error': 'هیچ شعری یافت نشد.'}, status=404)
        random_pk = random.choice(pks)
        poem = Poem.objects.select_related('poet', 'rhythm', 'work').prefetch_related('verses').get(pk=random_pk)
        return Response(PoemDetailSerializer(poem).data)


class VerseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Verse.objects.select_related('poem', 'poem__poet').all()
    serializer_class = VerseSerializer


class RhythmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rhythm.objects.all().order_by('name')
    serializer_class = RhythmSerializer
