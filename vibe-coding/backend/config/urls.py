from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'name': 'شعرخونه - تارنمای ادب و فرهنگ پارسی (SherKhaneh API)',
        'version': '1.0.0',
        'status': 'پایدار و برخط',
        'endpoints': {
            'auth': '/api/v1/auth/',
            'poetry': '/api/v1/poetry/',
            'library': '/api/v1/library/',
            'memorization': '/api/v1/memorization/',
            'mushaereh': '/api/v1/mushaereh/',
            'games': '/api/v1/games/',
            'daily': '/api/v1/daily/',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api_root, name='api_root'),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/poetry/', include('poetry.urls')),
    path('api/v1/library/', include('library.urls')),
    path('api/v1/memorization/', include('memorization.urls')),
    path('api/v1/mushaereh/', include('mushaereh.urls')),
    path('api/v1/games/', include('games.urls')),
    path('api/v1/daily/', include('daily_content.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
