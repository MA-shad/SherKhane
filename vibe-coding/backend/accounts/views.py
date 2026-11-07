from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens immediately upon registration
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'ثبت‌نام با موفقیت انجام شد.',
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure user profile exists
        profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'display_name': self.request.user.username}
        )
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile
        profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(UserSerializer(user).data)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
