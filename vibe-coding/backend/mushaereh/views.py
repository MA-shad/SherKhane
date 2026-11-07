import random
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import MushaerehRoom, MushaerehTurn
from .serializers import MushaerehRoomSerializer, SubmitVerseSerializer
from .services import submit_user_verse


class MushaerehRoomViewSet(viewsets.ModelViewSet):
    serializer_class = MushaerehRoomSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return MushaerehRoom.objects.filter(creator=user)
        return MushaerehRoom.objects.all().order_by('-created_at')[:10]

    def create(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        title = request.data.get('title', 'مسابقه با هوش سخن‌سنج')
        mode = request.data.get('mode', MushaerehRoom.Mode.BOT)

        # Initial random letter from common Persian letters
        initial_letters = ['م', 'ن', 'د', 'ر', 'ی', 'ب', 'ت', 'س', 'ک', 'ش']
        first_letter = random.choice(initial_letters)

        room = MushaerehRoom.objects.create(
            creator=user,
            title=title,
            mode=mode,
            current_letter=first_letter
        )
        serializer = self.get_serializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def play_turn(self, request, pk=None):
        """Submit a verse into the match and get authoritative arbiter decision"""
        room = self.get_object()
        serializer = SubmitVerseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user if request.user.is_authenticated else None
        result = submit_user_verse(room, serializer.validated_data['verse_text'], user=user)

        if not result['success']:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
