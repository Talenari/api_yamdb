from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .pagination import UserPagination
from .serializers import UserMeSerializer, UserSerializer, UserSignupSerializer


class UserSignupView(CreateAPIView):
    '''Класс создания пользователя по username и email.
    Пароль автоматически создается как код подтверждения, отсылаемый
    на почту.
    '''
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (permissions.AllowAny,)


class UserModelViewSet(ModelViewSet):
    """Просмотр и изменение профиля пользователей администратором."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = UserPagination
    permission_classes = (permissions.IsAdminUser,)


class UserMeModelView(APIView):
    """Просмотр и патч своего профиля пользователем."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)


class UserToken(APIView):
    """Функция создания и получения токена по username и confirmation_code."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            username = request.data['username']
        except KeyError:
            return Response(
                {"username": "Поле не указано"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            password = request.data['confirmation_code']
        except KeyError:
            return Response(
                {"confirmation_code": "Поле не указано"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not username:
            return Response(
                {"username": "Поле пустое"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                {"confirmation_code": "Поле пустое"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            token = RefreshToken.for_user(user)
            return Response(
                {'access': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {"Unauthorizer": "Пользователь с такими данными не найден"},
            status=status.HTTP_401_UNAUTHORIZED
        )
