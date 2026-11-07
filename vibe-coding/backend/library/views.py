from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Bookmark.objects.filter(user=self.request.user).select_related('poem', 'poem__poet', 'poem__rhythm')
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(category_tag=tag)
        return queryset

    @action(detail=False, methods=['delete'], url_path='by-poem/(?P<poem_id>[0-9]+)')
    def remove_by_poem(self, request, poem_id=None):
        deleted_count, _ = Bookmark.objects.filter(user=request.user, poem_id=poem_id).delete()
        if deleted_count > 0:
            return Response({'message': 'شعر از دفترچه شخصی حذف شد.'}, status=status.HTTP_200_OK)
        return Response({'error': 'شعر در دفترچه شما یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def tags(self, request):
        tags = Bookmark.objects.filter(user=request.user).values_list('category_tag', flat=True).distinct()
        return Response(list(tags))
