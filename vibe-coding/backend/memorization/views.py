from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from poetry.models import Poem
from .models import MemorizationItem
from .serializers import MemorizationItemSerializer, ReviewSubmissionSerializer
from .services import calculate_sm2_schedule, generate_cloze_challenge, generate_scramble_challenge


class MemorizationViewSet(viewsets.ModelViewSet):
    serializer_class = MemorizationItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MemorizationItem.objects.filter(user=self.request.user).select_related('poem', 'poem__poet', 'poem__rhythm')

    def create(self, request, *args, **kwargs):
        poem_id = request.data.get('poem') or request.data.get('poem_id')
        if not poem_id:
            return Response({'error': 'شناسه شعر الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)

        poem = Poem.objects.filter(id=poem_id).first()
        if not poem:
            return Response({'error': 'شعر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        item, created = MemorizationItem.objects.get_or_create(
            user=request.user,
            poem=poem
        )
        serializer = self.get_serializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def due_reviews(self, request):
        """Returns only cards that are due for review today or overdue"""
        due_items = [item for item in self.get_queryset() if item.is_due]
        serializer = self.get_serializer(due_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def submit_review(self, request):
        """Submit user review score (0-5) and advance the SM-2 schedule"""
        serializer = ReviewSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poem_id = serializer.validated_data['poem_id']
        quality_grade = serializer.validated_data['quality_grade']

        item = MemorizationItem.objects.filter(user=request.user, poem_id=poem_id).first()
        if not item:
            poem = Poem.objects.filter(id=poem_id).first()
            if not poem:
                return Response({'error': 'شعر یافت نشد.'}, status=404)
            item = MemorizationItem.objects.create(user=request.user, poem=poem)

        updated_item = calculate_sm2_schedule(item, quality_grade)
        return Response({
            'message': 'نتیجه مرور با موفقیت ثبت شد.',
            'item': MemorizationItemSerializer(updated_item).data
        })

    @action(detail=True, methods=['get'])
    def cloze_exercise(self, request, pk=None):
        """Generate fill-in-the-blank exercise for active recall"""
        item = self.get_object()
        exercise = generate_cloze_challenge(item.poem)
        return Response({
            'poem_id': item.poem.id,
            'title': item.poem.title,
            'poet': item.poem.poet.name,
            'exercises': exercise
        })

    @action(detail=True, methods=['get'])
    def scramble_exercise(self, request, pk=None):
        """Generate scrambled verse sequencing test"""
        item = self.get_object()
        exercise = generate_scramble_challenge(item.poem)
        return Response(exercise)
