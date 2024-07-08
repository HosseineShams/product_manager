from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status, views, permissions, response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from django.http import JsonResponse
from django.http import JsonResponse

class CreateUserView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return response.Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return response.Response({'error': 'Username is already taken'}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=username, password=password)
        return response.Response({'user_id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return response.Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return response.Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode and blacklist the token 
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Use the token's jti (JWT ID) as a unique identifier
            jti = token['jti']
            cache.set(jti, 'blacklisted', timeout=token.lifetime.total_seconds())

            return JsonResponse({'status': 'Token blacklisted successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

