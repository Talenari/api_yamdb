from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSignupSerializer


class UserSignupView(CreateAPIView):
    '''Класс создания пользователя по username и email.
    Пароль автоматически создается как код подтверждения, отсылаемый
    на почту.
    '''
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer


@api_view(['POST'])
def user_get_token(request):
    '''Функция создания и получения токена по username и verification_code'''
    try:
        username = request.data['username']
    except KeyError:
        return Response(
            {"username": "Поле не указано"},
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        password = request.data['verification_code']
    except KeyError:
        return Response(
            {"verification_code": "Поле не указано"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if username == '' or None:
        return Response(
            {"username": "Поле пустое"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if password == '' or None:
        return Response(
            {"password": "Поле пустое"},
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
