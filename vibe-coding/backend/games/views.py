from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import GameSession
from .serializers import GameSessionSerializer
from .services import (
    generate_guess_poet,
    generate_next_couplet,
    generate_word_quiz,
    generate_bait_chin_game
)


class GamesViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def guess_poet(self, request):
        challenge = generate_guess_poet()
        if not challenge:
            return Response({'error': 'بانک اشعار برای بازی کافی نیست.'}, status=400)
        return Response(challenge)

    @action(detail=False, methods=['get'])
    def next_couplet(self, request):
        challenge = generate_next_couplet()
        if not challenge:
            return Response({'error': 'بانک اشعار برای بازی کافی نیست.'}, status=400)
        return Response(challenge)

    @action(detail=False, methods=['get'])
    def word_quiz(self, request):
        challenge = generate_word_quiz()
        return Response(challenge)

    @action(detail=False, methods=['get'])
    def bait_chin(self, request):
        challenge = generate_bait_chin_game()
        if not challenge:
            return Response({'error': 'شعری برای بیت‌چین یافت نشد.'}, status=400)
        return Response(challenge)

    @action(detail=False, methods=['post'])
    def submit_score(self, request):
        """Record score and reward user XP"""
        game_type = request.data.get('game_type')
        score = int(request.data.get('score', 0))

        user = request.user if request.user.is_authenticated else None
        session = GameSession.objects.create(
            user=user,
            game_type=game_type or GameSession.GameType.GUESS_POET,
            score=score,
            is_completed=True
        )

        if user and hasattr(user, 'profile'):
            user.profile.add_xp(score)

        return Response({
            'message': 'امتیاز با موفقیت ثبت گردید.',
            'session': GameSessionSerializer(session).data
        })
