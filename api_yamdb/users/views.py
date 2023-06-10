from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.pagination import UserPagination
from users.permissions import AdminPermission
from users.serializers import (UserMeSerializer,
                               UserSerializer,
                               UserSignupSerializer)


class UserSignupView(APIView):
    '''Класс создания пользователя по username и email.
    Пароль автоматически создается как код подтверждения, отсылаемый
    на почту.
    '''
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.data.get('username') == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=request.data.get('email'),
                               username=request.data.get('username')):
            user = User.objects.get(email=request.data.get('email'))
            password = User.objects.make_random_password(length=32)
            user.password = make_password(password)
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения {password}.',
                'from@example.com',
                [f'{user.email}'],
            )
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = User.objects.make_random_password(length=32)
            serializer.save(password=make_password(password))
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения {password}.',
                'from@example.com',
                [f'{serializer.data["email"]}'],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserModelViewSet(ModelViewSet):
    """Просмотр и изменение профиля пользователей администратором."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = UserPagination
    permission_classes = (AdminPermission,)


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


class UserTokenView(APIView):
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
        check_password = user.check_password(password)

        if not check_password:
            return Response(
                {"confirmation_code": "Неверное поле"},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = RefreshToken.for_user(user)
        return Response(
            {'access': str(token.access_token)},
            status=status.HTTP_200_OK
        )
