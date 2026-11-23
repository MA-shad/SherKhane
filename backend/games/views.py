from django.shortcuts import render
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MoshaerehSession
from .serializers import MoshaerehSessionSerializer

from .serializers import (
    MoshaerehSessionSerializer,
    PlayTurnInputSerializer,
    PlayTurnResponseSerializer,
)

from .services.moshaereh import play_moshaereh_turn



FIRST_LETTER_POOL = [
    'الف', 'ب', 'ت', 'د', 'ر', 'ز', 'س', 'ش',
    'ع', 'ف', 'ک', 'گ', 'ل', 'م', 'ن', 'و', 'ه', 'ی'
]


class StartMoshaerehView(APIView):
    def post(self, request):
        initial_letter = random.choice(FIRST_LETTER_POOL)
        session = MoshaerehSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            current_letter=initial_letter,         
            score=0,
            round_count=0,
            is_active=True,
        )
        serializer = MoshaerehSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlayMoshaerehTurnView(APIView):
    def post(self, request, session_id):
        try:
            session = MoshaerehSession.objects.get(id=session_id)
        except MoshaerehSession.DoesNotExist:
            return Response({"detail": "بازی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        input_serializer = PlayTurnInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)

        verse_text = input_serializer.validated_data['verse_text']
        success, message, bot_verse = play_moshaereh_turn(session, verse_text)

        response_data = {
            'success': success,
            'message': message,
            'bot_verse': bot_verse,
            'session': session,
        }
        output_serializer = PlayTurnResponseSerializer(response_data)
        http_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response(output_serializer.data, status=http_status)


class MoshaerehDetailView(APIView):
    def get(self, request, session_id):
        try:
            session = MoshaerehSession.objects.get(id=session_id)
        except MoshaerehSession.DoesNotExist:
            return Response({"detail": "بازی یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        serializers = MoshaerehSessionSerializer(session)
        return Response(serializers.data, status=status.HTTP_200_OK)