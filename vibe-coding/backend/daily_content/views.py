from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DailyHighlight
from .services import get_or_create_today_highlight, draw_fal_hafez


class DailyContentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def today(self, request):
        highlight = get_or_create_today_highlight()
        return Response({
            'date': highlight.date,
            'beyt_of_day': {
                'first_couplet': highlight.beyt_first,
                'second_couplet': highlight.beyt_second,
                'poet': highlight.poet_name,
                'commentary': highlight.poetic_commentary
            },
            'proverb_of_day': {
                'proverb': highlight.proverb,
                'meaning': highlight.proverb_meaning,
                'origin': highlight.proverb_origin
            }
        })

    @action(detail=False, methods=['get'])
    def fal_hafez(self, request):
        fal = draw_fal_hafez()
        if not fal:
            return Response({'error': 'متن اشعار دیوان حافظ در دسترس نیست.'}, status=400)
        return Response(fal)
